from odoo import models, fields, api

class LoanInstallment(models.Model):
    _name = 'loan.installment'
    _description = 'Loan Installment Schedule'

    loan_id = fields.Many2one('loan.management', string='Loan', required=True, ondelete='cascade')
    due_date = fields.Date(string='Due Date', required=True)
    amount_due = fields.Float(string='Amount Due', required=True)
