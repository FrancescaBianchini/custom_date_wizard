from odoo import models, fields, api

class CustomerDateWizard(models.TransientModel):
    _name = 'customer.date.wizard'
    _description = 'Customer Filter by Date Range'

    date_from = fields.Date(string="From", required=True)
    date_to = fields.Date(string="To", required=True)

    def action_get_customers(self):
        domain = ['|']

        domain += [('invoice_ids.invoice_date', '>=', self.date_from),
                   ('invoice_ids.invoice_date', '<=', self.date_to)]

        domain += [('sale_order_ids.date_order', '>=', self.date_from),
                   ('sale_order_ids.date_order', '<=', self.date_to)]

        partners = self.env['res.partner'].search(domain)

        return {
            'name': 'Customers',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', partners.ids)],
        }
