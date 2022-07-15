from odoo import fields, models, api


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    attachment2_ids = fields.Many2many(
        'ir.attachment', 'mail_compose_message_2_ir_attachments_rel',
        'wizard_id', 'attachment_id', 'Attach file from attachments',
        domain="[('res_id', '=', res_id), ('res_model', '=', model)]")

    @api.onchange("attachment2_ids")
    def _onchange_attachment2_ids(self):
        if not self.attachment2_ids:
            return
        return {
            "value": {
                "attachment_ids": self.attachment2_ids + self.attachment_ids
            }
        }

