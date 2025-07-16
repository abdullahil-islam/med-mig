from odoo import api, fields, models, exceptions
import ast

class NVTDataTarget(models.Model):
    _name = 'nvt.data.target'
    _description = 'Data Target'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Name', required=True)
    data_source_id = fields.Many2one('nvt.data.source', string='Data Source')    
    query = fields.Text(string="Query")
    allow_parcial_transaction = fields.Boolean(string="Allow Parcial Transaction")
    origin_primary_key = fields.Char(string="Origin Primary Key")
    target_external_id = fields.Many2one('ir.model.fields', 'Target External Id', required=True,  ondelete='cascade', domain="[('model_id', '=', model_id)]")
    model_id = fields.Many2one('ir.model', 'Target Model', required=True, ondelete='cascade')
    field_ids = fields.One2many('nvt.data.target.field', 'target_id', 'Fields')

    result = fields.Text(string='Query Result')

    def button_sync_data(self):
        self.ensure_one()

        headers, rows = self.data_source_id.execute_query(self.query)

        # Let's assume your target model has a field called 'external_id'
        # which corresponds to 'origin_primary_key' in the source database.
        for row_data in rows:
            row = dict(zip(headers, row_data))
            # Here, you will have to map each column to the corresponding field in the Odoo model.
            # The exact logic will depend on how 'field_ids' is structured.
            vals = {}
            vals[self.target_external_id.name] = row[self.origin_primary_key]
            for field in self.field_ids:
                if field.origin_column_type == 'column':
                    vals[field.field_id.name] = row[field.origin_column]
                elif field.origin_column_type == 'column_int':
                    vals[field.field_id.name] = int(row[field.origin_column])
                elif field.origin_column_type == 'column_float':
                    vals[field.field_id.name] = float(row[field.origin_column])
                elif field.origin_column_type == 'column_m2m':
                    vals[field.field_id.name] = ast.literal_eval(field.origin_column)
                elif field.origin_column_type == 'fixed':
                    vals[field.field_id.name] = field.origin_column
                elif field.origin_column_type == 'fixed_ref':
                    vals[field.field_id.name] = int(field.origin_column)
                elif field.origin_column_type == 'formula':
                    pass
                elif field.origin_column_type == 'm2o_external_code':
                    origin_v, target_f = field.origin_column.split(',')
                    existing_rel = self.env[field.field_id.relation].search([(target_f, '=', row[origin_v])])
                    if existing_rel:
                        vals[field.field_id.name] = existing_rel[0].id
                    pass

            # Fetch existing record using primary key
            existing_record = self.env[self.model_id.model].search([(self.target_external_id.name, '=', row[self.origin_primary_key])])

            try:
                with self.env.cr.savepoint():
                    if existing_record:
                        existing_record.write(vals)
                    else:
                        self.env[self.model_id.model].create(vals)
                
            except Exception as e:
                self.message_post(body=f"Error Saving data {row}")
                
                if not self.allow_parcial_transaction:
                    raise exceptions.UserError(f"Error Saving data {row}: {str(e)}")
                
        self.message_post(body=f"Success full data migration")
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Your data migration was successful!',
                'sticky': False,  # True/False to stick the message, default is False
                'type': 'success',  # can be 'info', 'warning', 'success', 'danger'
            },
        }



    def action_show_query_result(self):
        self.ensure_one()

        headers, rows = self.data_source_id.execute_query(self.query + " limit 10")

        # Generate HTML table from the results
        table_html = self._generate_html_table(headers, rows)

        self.result = table_html

    def _generate_html_table(self, headers, rows):
        table_html = "<table border='1' class='o_list_table table table-sm table-hover position-relative table-striped'>"

        # Add headers
        table_html += "<thead><tr>"
        for header in headers:
            table_html += f"<th>{header}</th>"
        table_html += "</tr></thead>"

        # Add rows
        table_html += "<tbody>"
        for row in rows:
            table_html += "<tr>"
            for cell in row:
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>"
        table_html += "</tbody>"
        
        table_html += "</table>"
        return table_html
