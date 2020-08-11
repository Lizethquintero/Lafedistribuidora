# -*- coding: utf-8 -*-
# Copyright 2019 Juan Camilo Zuluaga Serna <Github@camilozuluaga>
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoice(models.Model):
	_inherit = "account.move"

	discrepancy_response_code_id   = fields.Many2one(
		comodel_name='account.invoice.discrepancy.response.code',
		string='Correction concept for Refund Invoice',)

	refund_type = fields.Selection(
		[('debit', 'Debit Note'),
		 ('credit', 'Credit Note')],
		index=True,
		string='Refund Type',
		track_visibility='always')



