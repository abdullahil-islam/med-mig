
from odoo import api, fields, models, _,tools


class InheritLeaveReport(models.Model):

    _inherit = 'hr.leave.report'

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_leave_report')

        self._cr.execute("""
            CREATE or REPLACE view hr_leave_report as (
                SELECT row_number() over(ORDER BY leaves.employee_id) as id,
                leaves.allocation_id as allocation_id, leaves.leave_id as leave_id,
                leaves.employee_id as employee_id, leaves.name as name,
                leaves.active_employee as active_employee, leaves.active as active,
                leaves.number_of_days as number_of_days, leaves.leave_type as leave_type,
                leaves.category_id as category_id, leaves.department_id as department_id,
                leaves.holiday_status_id as holiday_status_id, leaves.state as state,
                leaves.holiday_type as holiday_type, leaves.date_from as date_from,
                leaves.date_to as date_to, leaves.company_id
                from (select
                    allocation.active as active,
                    allocation.id as allocation_id,
                    null as leave_id,
                    allocation.employee_id as employee_id,
                    employee.active as active_employee,
                    allocation.private_name as name,
                    allocation.number_of_days as number_of_days,
                    allocation.category_id as category_id,
                    allocation.department_id as department_id,
                    allocation.holiday_status_id as holiday_status_id,
                    allocation.state as state,
                    allocation.holiday_type,
                    allocation.date_from as date_from,
                    allocation.date_to as date_to,
                    'allocation' as leave_type,
                    allocation.employee_company_id as company_id
                from hr_leave_allocation as allocation
                inner join hr_employee as employee on (allocation.employee_id = employee.id)
					WHERE allocation.holiday_status_id in (SELECT id from hr_leave_type 
                                WHERE date_to >= cast(now() as date))
                union all select
                    request.active as active,
                    null as allocation_id,
                    request.id as leave_id,
                    request.employee_id as employee_id,
                    employee.active as active_employee,
                    request.private_name as name,
                    (request.number_of_days * -1) as number_of_days,
                    request.category_id as category_id,
                    request.department_id as department_id,
                    request.holiday_status_id as holiday_status_id,
                    request.state as state,
                    request.holiday_type,
                    request.date_from as date_from,
                    request.date_to as date_to,
                    'request' as leave_type,
                    request.employee_company_id as company_id
                from hr_leave as request
                inner join hr_employee as employee on (request.employee_id = employee.id)
                WHERE request.state = 'validate' 
                        AND request.date_from >= (SELECT date_trunc('year', now())::date) 
                        AND request.date_to <= (SELECT (date_trunc('year', now()+ interval '1 year') - interval '1 day')::date)
                ) leaves
            );
        """)
