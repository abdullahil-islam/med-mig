from odoo import models, fields, api



class EngineerWiseReportView(models.AbstractModel):

    _name='report.misl_reports.report_engineer_wise_task_list'


    def _get_report_values(self, docids, data=None):

        engineer_id = self.env['res.users'].search([('id', '=', data['form']['engineer_id'])])
        company_id =  self.env['res.company'].search([('id', '=',data['form']['company_id'])])
        project_type = data['form']['project_type']
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']
        
        task_list = []
        query = """SELECT pt.id as id
                    FROM project_task pt 
                    inner join project_project p on p.id = pt.project_id
                    WHERE pt.id IN (
                    SELECT project_task_id
                    FROM project_task_res_users_rel
                    WHERE res_users_id = %s)""" % engineer_id.id
        if project_type == 'running':
            query += """ AND p.complete_project = false"""
        elif project_type == 'done':
            query += """ AND p.complete_project = true"""
        else:
            pass
        if start_date or end_date:
            query += """ AND pt.x_project_task_start_date >= '{}' AND pt.x_project_task_end_date <= '{}'""".format(start_date, end_date)
        q = self.env.cr.execute(query)
        all_tasks = self.env.cr.fetchall()
        all_tasks = [i[0] for i in all_tasks]

        for item in all_tasks:
            task = self.env['project.task'].search([('id','=',item)])
            task_dict = {
                'engineer_id': engineer_id.name,
                'project': task.project_id.name,
                'task': task.name,
                'stage': task.stage_id.name,
            }
        
            task_list.append(task_dict)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'engineer_id': engineer_id,
            'company_id' : company_id,
            'docs': task_list,
            'project_type': project_type,
            'start_date': start_date,
            'end_date': end_date

        }