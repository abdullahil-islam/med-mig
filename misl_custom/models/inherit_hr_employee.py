
from odoo import api, fields, models, _,tools


class InheritHrEmployee(models.Model):

    _inherit = 'hr.employee'
    
    def _get_remaining_leaves(self):
        """ Helper to compute the remaining leaves for the current employees
            :returns dict where the key is the employee id, and the value is the remain leaves
        """
        self._cr.execute("""
            SELECT
                sum(h.number_of_days) AS days,
                h.employee_id
            FROM
                (
                    SELECT holiday_status_id, number_of_days,
                        state, employee_id
                    FROM hr_leave_allocation
                    WHERE holiday_status_id in (SELECT id from hr_leave_type 
                                WHERE validity_stop >= cast(now() as date))
                    UNION ALL
                    SELECT holiday_status_id, (number_of_days * -1) as number_of_days,
                        state, employee_id
                    FROM hr_leave 
                         WHERE date_from >= (SELECT date_trunc('year', now())::date) 
					        AND date_to <= (SELECT (date_trunc('year', now()+ interval '1 year') - interval '1 day')::date)
                ) h
                join hr_leave_type s ON (s.id=h.holiday_status_id)
            WHERE
                s.active = true AND h.state='validate' AND
                (s.allocation_type='fixed' OR s.allocation_type='fixed_allocation') AND
                h.employee_id in %s
            GROUP BY h.employee_id""", (tuple(self.ids),))
        return dict((row['employee_id'], row['days']) for row in self._cr.dictfetchall())