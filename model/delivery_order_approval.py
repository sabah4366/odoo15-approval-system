from odoo import models, fields, api ,http

class DeliveryOrderApproval(models.Model):
    _name = 'inv_approval_system.delivery.approval'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Delivery  Approvals'

    name = fields.Char(string="Delivery Order Ref",readonly=True,store=True)
    partner_id = fields.Many2one("res.partner",string='Customer',readonly=True)
    delivery_order_date = fields.Datetime(string="Delivery Scheduled Date",readonly=True,store=True)
    state = fields.Char(string="Delivery State",readonly=True)
    delivery_source_documnt=fields.Char(string='Delievry Source Doc',readonly=True,store=True)
    delivery_product_ids = fields.One2many('inv_approval_system.products.ordered', 'delivery_approval_id', string='Products Ordered')
    is_approved=fields.Boolean(string="Approved",default=False)
    sequence_no=fields.Char(string='Sequence Number')


    def to_approve_delivery(self):
        domain=[('name','=',self.name)]
        delivered_item=self.env['stock.picking'].search(domain)
        delivered_item.write({
            'approval_or_not':'approved'
        })
        self.is_approved=True
        self.send_email_notification()

    def send_email_notification(self):
        mail_template = self.env.ref('inv_approval_system.email_template_approval')
        email_to = self.get_email_to()
        mail_template.email_to = email_to
        mail_template.send_mail(self.id, force_send=True)

    def get_email_to(self):
        stock_manager_group = self.env.ref('stock.group_stock_manager')
        email_list = [user.partner_id.email for user in stock_manager_group.users if user.partner_id.email]
        return ";".join(email_list)



class ProductsOrdered(models.Model):
    _name = 'inv_approval_system.products.ordered'
    _description = 'Products  Ordered'

    delivery_approval_id=fields.Many2one('inv_approval_system.delivery.approval',string='Approval')
    product_id=fields.Many2one('product.product',string="product",readonly=True,store=True)
    # product_id=fields.Char(string="product",readonly=True,store=True)
    quantity=fields.Integer(string='Quantity',readonly=True,store=True)
    uom=fields.Char(string='Uom',readonly=True,store=True)
