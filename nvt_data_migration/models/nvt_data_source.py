from odoo import  fields, models, exceptions
import psycopg2

class NVTDataSource(models.Model):
    _name = 'nvt.data.source'
    _description = 'Data Source'

    name = fields.Char('Name', required=True)
    host = fields.Char('Host', required=True)
    port = fields.Integer('Port', required=True)
    database = fields.Char('Database', required=True)
    user = fields.Char('User', required=True)
    password = fields.Char('Password', required=True)

    def execute_query(self, query):
        self.ensure_one()

        # Connect to PostgreSQL
        conn_params = {
            'dbname': self.database,
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': self.port
        }

        # Verificar se a query possui instruções proibidas
        forbidden_statements = ['UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']
        for statement in forbidden_statements:
            if statement in query.upper():
                raise exceptions.UserError(_('Queries containing %s are not allowed for security reasons.') % statement)

        
        try:
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            cur.execute(query)  # Assuming query is validated and safe from SQL injection
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
        except Exception as e:
            raise exceptions.UserError(f"Error executing the query: {str(e)}")
        finally:
            conn.close()

        return headers, rows
