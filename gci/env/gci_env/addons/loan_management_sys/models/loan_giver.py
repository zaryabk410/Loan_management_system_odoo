from odoo import models, fields, api

class LoanGiver(models.Model):
    _name = 'loan.giver'
    _description = 'Loan Giver'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    address = fields.Text(string='Address')
