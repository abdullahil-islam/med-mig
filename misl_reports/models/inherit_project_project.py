from odoo import models, fields, api


class InheritProjectProject(models.Model):
    _inherit = 'project.project'


    def print_project_wise_task_report(self):
        return self.env.ref('misl_reports.project_wise_task_report').report_action(self)
    

    def get_project_wise_task_list(self):
        for rec in self:
            task_list = []
            all_tasks = self.env['project.task'].search([('project_id','=',rec.id)])

            for task in all_tasks:

                user_str = ''
                users_list = []
                for user in task.user_ids:
                    users_list.append(user)
                    user_str = user_str + user.name
                    if len(task.user_ids) > 1 and not users_list.index(user) == len(task.user_ids)-1:
                        user_str = user_str + ', '

                task_dict = {
                    'task_name': task.name,
                    'assigned_to': user_str,
                    'stage': task.stage_id.name,
                }
            
                task_list.append(task_dict)
            return task_list
    

    # def print_engineer_wise_task_report(self,engineer_id):
    #      return self.env.ref('misl_reports.engineer_wise_task_report').report_action(self)



# class InheritProjectTask(models.Model):
#     _inherit = 'project.task'


#     def print_engineer_wise_task_report(self,engineer_id):
#         engineer_id = self.env['res.users'].search([('id', '=', engineer_id)])
#         return self.env.ref('misl_reports.engineer_wise_task_report').report_action(self, data=datas)
    

#     def get_engineer_wise_task_list(self,engineer_id):
#         for rec in self:
#             task_list = []
#             all_tasks = self.env['project.task'].search([])
#             for task in all_tasks:
#                 if engineer_id in task.user_ids:
#                     task_dict = {
#                         'engineer':engineer_id.name,
#                         'project': task.project_id.name,
#                         'task': task.name,
#                         'stage': task.stage_id.name,
#                     }
                
#                     task_list.append(task_dict)
#                     return task_list