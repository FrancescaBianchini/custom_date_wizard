from odoo import models, fields, api

class CustomerDateWizard(models.TransientModel):
    _name = 'customer.date.wizard'
    _description = 'Filter Customers by Documents in Date Range'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    line_ids = fields.One2many('customer.report.line', 'wizard_id', string="Risultati")

    def action_get_customers(self):
        # Pulizia precedente
        self.line_ids.unlink()

        AccountMove = self.env['account.move']
        SaleOrder = self.env['sale.order']

        # Fatture cliente non annullate nel range
        invoices = AccountMove.search([
            ('move_type', '=', 'out_invoice'),
            ('state', '!=', 'cancel'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
        ])

        # Ordini di vendita non annullati nel range
        orders = SaleOrder.search([
            ('state', '!=', 'cancel'),
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to),
        ])

        partner_data = {}

        # Fatture
        for inv in invoices:
            pid = inv.partner_id.id
            partner_data.setdefault(pid, {'invoices': 0, 'orders': 0, 'indirect': 0})
            partner_data[pid]['invoices'] += 1

        # Ordini
        for order in orders:
            # Cliente principale
            pid = order.partner_id.id
            partner_data.setdefault(pid, {'invoices': 0, 'orders': 0, 'indirect': 0})
            partner_data[pid]['orders'] += 1

            # Cliente indiretto
            if order.x_studio_cliente_indiretto:
                ind_pid = order.x_studio_cliente_indiretto.id
                partner_data.setdefault(ind_pid, {'invoices': 0, 'orders': 0, 'indirect': 0})
                partner_data[ind_pid]['indirect'] += 1

        # Crea le righe di report
        for pid, values in partner_data.items():
            self.env['customer.report.line'].create({
                'wizard_id': self.id,
                'partner_id': pid,
                'invoice_count': values['invoices'],
                'order_count': values['orders'],
                'indirect_order_count': values['indirect'],
            })

        return {
            'name': 'Clienti Coinvolti',
            'view_mode': 'tree',
            'res_model': 'customer.report.line',
            'type': 'ir.actions.act_window',
            'domain': [('wizard_id', '=', self.id)],
            'target': 'new',
        }
