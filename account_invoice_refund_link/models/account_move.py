# Copyright 2004-2011 Pexego Sistemas Informáticos. (http://pexego.es)
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2014-2018 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    refund_invoice_ids = fields.One2many(
        "account.move", "reversed_entry_id", string="Refund Invoices", readonly=True
    )

    @api.model
    def _reverse_move_vals(self, default_values, cancel=True):
        move_vals = super()._reverse_move_vals(default_values, cancel)
        if self.env.context.get("link_origin_line", False) and move_vals[
            "move_type"
        ] in (
            "out_refund",
            "in_refund",
        ):
            refund_lines_vals = move_vals.get("line_ids", [])
            for i, line in enumerate(self.line_ids):
                if i + 1 > len(refund_lines_vals):  # pragma: no cover
                    # Avoid error if someone manipulate the original method
                    break
                if not line.exclude_from_invoice_tab:
                    refund_lines_vals[i][2]["origin_line_id"] = line.id
        return move_vals
