from odoo import models, fields, api

class LoanRepayment(models.Model):
    _name = 'loan.repayment'
    _description = 'Loan Repayment Record'

    loan_id = fields.Many2one('loan.management', string='Loan', required=True, ondelete='cascade')
    repayment_date = fields.Date(string='Repayment Date', default=fields.Date.today, required=True)
    amount_paid = fields.Float(string='Amount Paid', required=True)
    loan_computed_name = fields.Char(string='Loan ID', compute='_compute_loan_computed_name', store=True)

    @api.depends('loan_id.computed_name')
    def _compute_loan_computed_name(self):
        for record in self:
            record.loan_computed_name = record.loan_id.computed_name if record.loan_id else ''

