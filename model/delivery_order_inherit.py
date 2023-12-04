from odoo import models, fields, api ,http
class StockPickingTypeInherit(models.Model):
    _inherit = 'stock.picking.type'

    need_accounts_approval=fields.Boolean(string='Need Accounts Approval')


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    approval_or_not = fields.Selection([
        ('waiting for approval', 'Waiting for Approval'),
        ('approved', 'Approved'),
    ], string='Approval Status', readonly=True, tracking=True)
    sent_approve = fields.Boolean(string='Is Approver', compute='_compute_is_approver')
    is_need_approve=fields.Boolean(string='Is Need Approve')
    sequence_no=fields.Char(string="Seq")

    def _compute_is_approver(self):
        for record in self:
                record.is_need_approve = False if record.picking_type_id.need_accounts_approval is True else True
                wytng_apprvl=record.approval_or_not == 'waiting for approval'
                record.sent_approve=False if wytng_apprvl is True  else True


    def sent_for_approval(self):
        product_values=[]
        for move in self.move_ids_without_package:
            product_values.append({
                'product_id': move.product_id.id,
                'quantity': move.product_uom_qty,
                'uom': move.product_uom.name,
            })
        self.sequence_no=self.env['ir.sequence'].next_by_code('inv_approval_system.stock.picking')
        vals = {
            'name': self.name,
            'partner_id': self.partner_id.id,
            'delivery_order_date': self.scheduled_date,
            'state': 'Ready',
            'delivery_source_documnt': self.origin,
            'delivery_product_ids': [(0, 0, product_data) for product_data in product_values],
            'sequence_no': self.sequence_no
        }
        print('vals',vals['sequence_no'],vals['delivery_source_documnt'])

        self.approval_or_not = 'waiting for approval'
        self.env['inv_approval_system.delivery.approval'].create(vals)
        self.send_email_notification()


    def send_email_notification(self):
        mail_template = self.env.ref('inv_approval_system.email_template_delivery_items')
        email_to = self.get_email_to()
        mail_template.email_to = email_to
        mail_template.send_mail(self.id, force_send=True)

    def get_email_to(self):
        group_accountant_accountant = self.env.ref('account.group_account_user')
        group_accountant_advisor = self.env.ref('account.group_account_manager')
        group_ids = [group_accountant_accountant.id, group_accountant_advisor.id]
        group_users = self.env['res.users'].search([('groups_id', 'in', group_ids)])
        email_list = [user.partner_id.email for user in group_users if user.partner_id.email]
        return ";".join(email_list)