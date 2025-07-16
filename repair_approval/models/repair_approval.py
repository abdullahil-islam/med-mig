# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class RepairApproval(models.Model):
    _name = "repair.hierarchy"

    name = fields.Char("Name")
    repair_hir_ids = fields.One2many(
        "repair.hierarchy.line", "repair_hi_id", string="Approval Hierarchy"
    )


class RepairApprovalLine(models.Model):
    _name = "repair.hierarchy.line"
    _order = "sequence asc"

    sequence = fields.Integer("Sequence")
    user_ids = fields.Many2many("res.users")
    repair_hi_id = fields.Many2one("repair.hierarchy", string="Repair Approval")
    next_stage_id = fields.Many2one(
        "repair.hierarchy.line", compute="_compute_next_stage_id", string="Next Stage"
    )

    def _compute_next_stage_id(self):
        for rec in self:
            rec = rec.sudo()
            current_sequence = rec.sequence
            next_stage = rec.search(
                [
                    ("sequence", ">", current_sequence),
                ],
                limit=1,
            )
            rec.next_stage_id = next_stage.id if next_stage else False


class RepairOrder(models.Model):
    _inherit = "repair.order"

    def _get_default_approval_config_line_id(self):
        repair_app_id = self.env.ref(
            "repair_approval.repair_approval_record", raise_if_not_found=False
        )
        return (
            repair_app_id.repair_hir_ids.search([], limit=1, order="sequence asc")
            if repair_app_id
            else False
        )

    approval_ids = fields.Many2many(
        "res.users", related="approval_config_line_id.user_ids", string="Approval Users"
    )
    repair_last_approver_id = fields.Many2one("res.users")
    approval_config_line_id = fields.Many2one(
        "repair.hierarchy.line", default=_get_default_approval_config_line_id
    )
    next_stage_id = fields.Many2one(
        "repair.hierarchy.line", related="approval_config_line_id.next_stage_id"
    )
    approval_pending = fields.Boolean(
        "Approval Pending", compute="_display_approve_button"
    )
    repair_last_approver = fields.Html(
        string="Last Approval String", compute="_display_approve_button"
    )
    display_validate_button = fields.Boolean(
        "Display Validate Button", compute="_display_approve_button"
    )
    type_readonly = fields.Boolean(compute="_compute_type_readonly")

    def _display_approve_button(self):
        for rec in self:
            rec.approval_pending = False
            tags = rec.tag_id.mapped("name")
            if "Govt" in tags:
                rec.display_validate_button = True
                rec.repair_last_approver = ""
            else:
                if (
                    rec.approval_ids
                    and (rec.state == "confirmed" or (rec.state == 'ready' and rec.invoice_method == 'b4repair'))
                    and rec.type == "on_call"
                ):
                    rec.display_validate_button = False
                else:
                    rec.display_validate_button = True
                repair_last_approver = ""
                if rec.repair_last_approver_id:
                    repair_last_approver += "Last Approved by : " + str(
                        rec.repair_last_approver_id.name
                    )
                    if rec.approval_ids:
                        rec.display_validate_button = False
                        repair_last_approver += " <br/>Waiting approval from: "
                        for one_approval in rec.approval_ids:
                            repair_last_approver += str(one_approval.name) + ", "
                    else:
                        rec.display_validate_button = True
                rec.repair_last_approver = repair_last_approver
                if (
                    (rec.state == "confirmed" or (rec.state == 'ready' and rec.invoice_method == 'b4repair'))
                    and self.env.user.id in rec.sudo().approval_ids.ids
                    and rec.type == "on_call"
                ):
                    rec.approval_pending = True

    @api.depends("product_id.equipment_id.type")
    def _compute_type_readonly(self):
        for rec in self:
            if rec.product_id.equipment_id.type == "on_call":
                rec.type_readonly = True
            else:
                rec.type_readonly = False

    def repair_approval(self):
        self.ensure_one()
        tags = self.tag_id.mapped("name")
        repair_app_id = self.env.ref("repair_approval.repair_approval_record")
        if (
            repair_app_id
            and (self.state == "confirmed" or (self.state == 'ready' and self.invoice_method == 'b4repair'))
            and self.type == "on_call" and "Govt" not in tags
            and self.next_stage_id
        ):
            next_stage_id = self.next_stage_id
            self.approval_config_line_id = next_stage_id.id
            if next_stage_id and next_stage_id.user_ids:
                self.repair_last_approver_id = self.env.user.id
                self.message_post(
                    body=_(
                        "<p><strong><span class='fa fa-sun-o'></span></strong> <span>Repair Approval</span> done by <span> "
                        + str(self.env.user.name)
                        + "</span></p>"
                    )
                )
                if self.approval_ids:
                    email_ids = ",".join([i.email for i in self.approval_ids])
                    mail_template = self.env.ref(
                        "repair_approval.email_template_repair_order_teamhead"
                    )
                    mail_template.send_mail(
                        self.id, force_send=True, email_values={"email_to": email_ids}
                    )
                return True

        self.repair_last_approver_id = self.env.user.id
        self.message_post(
            body=_(
                "<p><strong><span class='fa fa-sun-o'></span></strong> <span>Repair Approval</span> done by <span> "
                + str(self.env.user.name)
                + "</span></p>"
            )
        )
        self.approval_config_line_id = False
        return True

    def action_validate(self):
        result = super(RepairOrder, self).action_validate()

        repair_app_id = self.env.ref("repair_approval.repair_approval_record")
        if (
            repair_app_id
            and self.type == "on_call"
            and self.approval_config_line_id
            and self.approval_config_line_id.user_ids
        ):
            email_ids = ",".join(
                [i.email for i in self.approval_config_line_id.user_ids]
            )
            mail_template = self.env.ref(
                "repair_approval.email_template_repair_order_teamhead"
            )
            mail_template.send_mail(
                self.id, force_send=True, email_values={"email_to": email_ids}
            )

        return result
