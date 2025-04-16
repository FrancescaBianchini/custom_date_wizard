from odoo import models, fields

class CustomerReportLine(models.TransientModel):
    _name = 'customer.report.line'
    _description = 'Temporary Customer Report Line'

    wizard_id = fields.Many2one('customer.date.wizard', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string="Cliente", readonly=True)
    invoice_count = fields.Integer(string="N. Fatture", readonly=True)
    order_count = fields.Integer(string="N. Ordini", readonly=True)
    indirect_order_count = fields.Integer(string="N. Ordini Indiretti", readonly=True)
