from odoo import models, fields, api

class LoanManagement(models.Model):
    _name = 'loan.management'
    _description = 'Loan Management System'
    _inherit = ['mail.thread' , 'mail.activity.mixin']

    # User Information Fields
    loan_sequence = fields.Char(string='Loan Sequence', required=True, copy=False, readonly=True, default='/')
    name = fields.Char(string='Name', required=True , tracking=True)
    father_name = fields.Char(string="Father's Name", required=True , tracking=True)
    email = fields.Char(string='Email', required=True , tracking=True)
    phone = fields.Char(string='Phone', required=True)
    address = fields.Text(string='Address')
    cnic_number = fields.Char(string='CNIC Number', required=True , tracking=True)

    # Loan Details Fields
    loan_purpose = fields.Char(string='Purpose of Loan', required=True , tracking=True)
    loan_amount = fields.Float(string='Loan Amount', required=True,tracking=True)
    loan_date = fields.Date(string='Loan Date', default=fields.Date.today, required=True , tracking=True)
    # giver_id = fields.Many2one('loan.giver', string="Loan Giver", required=True, tracking=True)
    giver_id = fields.Many2one('loan.giver', string="Loan Giver", required=True, tracking=True)
    giver_phone = fields.Char(string="Giver Phone Number", readonly=True)

    @api.onchange('giver_id')
    def _onchange_giver_id(self):
        for record in self:
            record.giver_phone = record.giver_id.phone if record.giver_id else ''

    # Installment and Repayment Fields
    total_installments = fields.Integer(string='Number of Installments', required=True,tracking=True)
    duration_months = fields.Integer(string='Duration (in months)', required=True,tracking=True)
    installment_amount = fields.Float(string='Installment Amount', compute='_compute_installment_amount', store=True,tracking=True)
    remaining_balance = fields.Float(string='Remaining Balance', compute='_compute_remaining_balance', store=True,tracking=True)

    repayment_ids = fields.One2many('loan.repayment', 'loan_id', string='Repayments',tracking=True)
    installment_schedule = fields.One2many('loan.installment', 'loan_id', string='Installment Schedule')

    # Workflow state field
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('running', 'Running'),
        ('complete', 'Complete')
    ], string='State', default='draft', required=True)

    def action_approve(self):
        self.state = 'approved'

    def action_start(self):
        self.state = 'running'

    def action_complete(self):
        self.state = 'complete'

    #     sequence id
    # @api.model
    # def create(self, vals):
    #     if vals.get('loan_sequence', '/') == '/':
    #         vals['loan_sequence'] = self.env['ir.sequence'].next_by_code(
    #             'loan.management') or '/'
    #     return super(LoanManagement, self).create(vals)

    # Computed Field
    computed_name = fields.Char(string='Computed Name', compute='_compute_computed_name', store=True)

    @api.depends('loan_sequence', 'name')
    def _compute_computed_name(self):
        for record in self:
            record.computed_name = f"{record.loan_sequence} - {record.name}" if record.loan_sequence and record.name else ''

    @api.depends('loan_amount', 'total_installments')
    def _compute_installment_amount(self):
        for record in self:
            record.installment_amount = record.loan_amount / record.total_installments if record.total_installments else 0

    @api.depends('loan_amount', 'repayment_ids.amount_paid')
    def _compute_remaining_balance(self):
        for record in self:
            total_paid = sum(record.repayment_ids.mapped('amount_paid'))
            record.remaining_balance = record.loan_amount - total_paid
            if record.state == 'running' and record.remaining_balance == 0:
                record.state = 'complete'

    # @api.model
    # def create(self, vals):
    #     if vals.get('loan_sequence', '/') == '/':
    #         vals['loan_sequence'] = self.env['ir.sequence'].next_by_code(
    #             'loan.management') or '/'
    #     return super(LoanManagement, self).create(vals)
    #
    #     loan = super().create(vals)
    #     installment_amount = loan.installment_amount
    #     for i in range(loan.total_installments):
    #         self.env['loan.installment'].create({
    #                 'loan_id': loan.id,
    #                 'due_date': fields.Date.add(loan.loan_date, months=i),
    #                 'amount_due': installment_amount,
    #          })
    #     return loan
    @api.model
    def create(self, vals):
        # Generate the loan sequence if not provided
        if vals.get('loan_sequence', '/') == '/':
            vals['loan_sequence'] = self.env['ir.sequence'].next_by_code(
                'loan.management') or '/'

        # Create the loan record
        loan = super(LoanManagement, self).create(vals)

        # Generate loan installments
        installment_amount = loan.installment_amount
        for i in range(loan.total_installments):
            self.env['loan.installment'].create({
                'loan_id': loan.id,
                'due_date': fields.Date.add(loan.loan_date, months=i),
                'amount_due': installment_amount,
            })

        return loan


class LoanReport(models.AbstractModel):
        _name = 'report.loan_management.loan_report'
        _description = 'Loan Details and Repayment Schedule Report'

        @api.model
        def _get_report_values(self, docids, data=None):
            docs = self.env['loan.management'].browse(docids)
            return {
                'docs': docs,
            }



