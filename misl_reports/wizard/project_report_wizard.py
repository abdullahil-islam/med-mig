from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import pytz


class ProjectReportWizard(models.TransientModel):
    """Transient model to Print Project Report"""

    _name = "project.report.wizard"
    _description = "Print Project Reports"


    company_id = fields.Many2one('res.company', string='Company')

    report_type = fields.Selection([('engineer', 'Engineer Wise Report'),('project', 'Project Wise Report')], string="Report Type", required=True)
    engineer_id = fields.Many2one('res.users', string="Engineer",  domain=lambda self: [("groups_id", "=",
                                                  self.env.ref("repair_maintenance.group_maintenance_technician").id)])
    project_id = fields.Many2one('project.project', string="Project")
    time_frame = fields.Boolean('Duration')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    type = fields.Selection(
        [
            ('running', 'Running'),
            ('done', 'Done'),
            ('all', 'All')
        ], string='Project Status', default='all', required=True
    )

    @api.onchange('type')
    def onchange_type(self):
        self.ensure_one()
        self.project_id = None
        if self.type == 'running':
            return {'domain': {'project_id': [('complete_project', '=', False)]}}
        elif self.type == 'done':
            return {'domain': {'project_id': [('complete_project', '=', True)]}}
        else:
            return {'domain': {'project_id': []}}

    def print_engineer_wise_report(self):
        self.company_id = self.engineer_id.company_id
        start_date = False
        end_date = False

        if self.from_date:
            start_date = str(self.from_date - timedelta(days=1)) + " 18:00:00"

        if self.to_date:
            end_date = str(self.to_date) + " 17:59:59"
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'engineer_id': self.engineer_id.id,
                'company_id': self.company_id.id,
                'project_type': self.type,
                'start_date': start_date,
                'end_date': end_date
            },
        }
        return self.env.ref('misl_reports.engineer_wise_task_report').report_action(self, data=data)
    
    def print_project_wise_report(self):
        active_id = self.env['project.project'].browse(self._context.get('active_ids', [self.project_id.id]))
        self.company_id = active_id.company_id
        return active_id.print_project_wise_task_report()
