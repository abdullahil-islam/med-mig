# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)


class TaskWizard(models.TransientModel):
    _name = 'task.wizard.assigntotask'
    _description = 'Task Assign'
    
    user_ids = fields.Many2many('res.users', string="Users")
    
    
    def action_task_assigntotask(self):
        for res in self:
            records = self.env['project.task'].browse(self._context.get('active_ids', list()))
            for rec in records:
                rec.user_ids = [(6,0,res.user_ids.ids)]
            return True


class ProjectTaskTemplate(models.Model):

    _name = 'project.task.template'
    _inherit = 'project.task'

    depend_on_ids = fields.Many2many('project.task', relation="task_tmpl_dependencies_rel", column1="task_id",
                                     column2="depends_on_id", string="Blocked By", tracking=True, copy=False,
                                     domain="[('project_id', '!=', False), ('id', '!=', id)]")
    dependent_ids = fields.Many2many('project.task', relation="task_tmpl_dependencies_rel", column1="depends_on_id",
                                     column2="task_id", string="Block", copy=False,
                                     domain="[('project_id', '!=', False), ('id', '!=', id)]")

    user_ids = fields.Many2many('res.users', relation='project_task_tmpl_user_rel', column1='task_tmpl_id', column2='user_id',
                                string='Assignees', context={'active_test': False}, tracking=True)

    personal_stage_type_ids = fields.Many2many('project.task.type', 'project_task_tmpl_type_rel', column1='task_tmpl_id',
                                               column2='stage_id',
                                               ondelete='restrict', group_expand='_read_group_personal_stage_type_ids',
                                               copy=False,
                                               domain="[('user_id', '=', user.id)]", depends=['user_ids'],
                                               string='Personal Stage')

    use_as_template = fields.Boolean(
        string="Active",
        default=True,
        help="Set to use this template.",
    )
    default_stage_id = fields.Many2one(
        'project.task.type',
        string="Default Stage",
        help="Created task will be put selected stage.",
    )
    name_of_equipment = fields.Selection(
        [('mri', 'MRI-'), ('ct', 'CT-'), ('xr', 'XR-'), ('usg', 'USG-'), ('cr', 'CR-'), ('fpd', 'FPD-'),
         ('mam', 'MAM-'),
         ('bmd', 'BMD-'), ('opg', 'OPG-'), ('crm', 'CRM-'), ('prt', 'PRT-'), ('omprt', 'PRTOM-')],
        string="Name Of Equipment")

    
    def toggle_template(self):
        """ Inverse the value of the field ``use_as_template`` on the records in ``self``. """
        for record in self:
            record.use_as_template = not record.use_as_template


class ProjectProject(models.Model):

    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        res = super(ProjectProject, self).create(vals)
        templates = self.env['project.task.template'].search([
            ('use_as_template', '=', True),
            ('name_of_equipment', '=', res.name_of_equipment),
        ])
        self.env.ref('repair_maintenance.project_task_type_pre_installation').project_ids = [(6, 0,[res.id])]
        self.env.ref('repair_maintenance.project_task_type_installation').project_ids = [(6, 0, [res.id])]
        self.env.ref('repair_maintenance.project_task_type_post_installation').project_ids = [(6, 0, [res.id])]
        self.env.ref('repair_maintenance.project_task_type_hand_over').project_ids = [(6, 0, [res.id])]

        ProjectTask = self.env['project.task']
        for template in templates:
            vals = {}
            fields_data = template.fields_get()
            skip_fields = (
                'project_id',
                'message_follower_ids',
                'id',
                'write_date',
                'create_data',
                'use_as_template',
                'message_ids',
                'default_stage_id',
                'child_ids',
		'timesheet_ids',
            )
            for field_data in fields_data:
                if field_data not in skip_fields:
                    value = template.__getattribute__(field_data)
                    if fields_data[field_data]['type'] == 'one2many':
                        vals[field_data] = value.mapped('id')
                    elif fields_data[field_data]['type'] == 'many2one':
                        vals[field_data] = value.id
                    elif fields_data[field_data]['type'] == 'many2many':
                        vals[field_data] = [[6, 0, value.mapped('id')]]
                    else:
                        vals[field_data] = value
            vals.update({
                'stage_id': template.default_stage_id.id,
                'project_id': res.id,
                'user_id': self.env.user.id
            })
            _logger.warning("-create_vals-- : %s", vals)
            ProjectTask.create(vals)
        return res
