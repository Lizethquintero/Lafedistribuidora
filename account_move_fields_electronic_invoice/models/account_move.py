# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import AccessDenied
from collections import defaultdict
from odoo.exceptions import ValidationError
from odoo import fields, models
from odoo.tools import float_is_zero

logger = logging.getLogger(__name__)

class AccountPaymentInhenit(models.TransientModel):
    _inherit = 'account.payment.register'
    
    import_total = fields.Float('Importe Total', compute="_compute_total_import")
    
    @api.depends('invoice_ids')
    def _compute_total_import(self):
        logger.info('******************************IMPORT TOTAAAL***********************************')
        amount_total = 0
        for record in self:
            for invoices in record.invoice_ids:
                amount_total += invoices.amount_residual_signed
        
        logger.info('***************IMPOR TOTAL ENTRANCE*****************************************')
        logger.info(amount_total)
        
        record.import_total = amount_total

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    method_la_fe_id = fields.Many2one('payment.methods.la.fe', string='Forma de pago',compute='_compute_method_la_fe_id' )
    delivery_adress_shipping = fields.Char(
        'Domicilio de entrega', compute='_compute_partner_delivery_adress_shipping')
    zip_shipping_id = fields.Many2one(
        'res.city.zip', string='Ubicación zip entrega',compute='_compute_partner_delivery_zip_shipping')
    
    @api.onchange('currency_id')
    def compute_date_life(self):
        c=0
        for lines in self.invoice_line_ids:
            exp_dates=[]
            line = lines.lot_id.replace("\n","")
            line = line.split(",")
            line_exp = lines.life_date.replace("\n","")
            line_exp = line_exp.split(",")
            logger.info('******************************************exp_dates*****************************')
            logger.info(line)
            """
            if len(line_exp) >=2:
                for line in line_exp:
                    logger.info('******************************************exp_dates*****************************')
                    logger.info(line)
                    exp_dates.append(line)
            else:
                logger.info('******************************************exp_dates*****************************')
                logger.info(line_exp[0])
                exp_dates.append(line_exp[0])
            """
            
            if len(line)>=2:
                for lot in line:
                    logger.info('******************************************1*****************************')
                    logger.info(line)
                    logger.info('******************************************2*****************************')
                    logger.info(line)
                    lot=str(lot)
                    logger.info(lot)
                    lot=lot.split(" ")
                    logger.info(lot)
                    lines.write({'lot_segment': lot[0]})
                        
            else:
                lines.write({'lot_segment': line[0]})
        
        """
        #exp_dates=sorted(set(exp_dates))
        
        
        logger.info('******************************************exp_dates*****************************')
        logger.info(exp_dates)
        c=0
        logger.info('******************************************exp_dates*****************************')
        logger.info(len(self.invoice_line_ids))
        if c <= len(self.invoice_line_ids):
            for date_life in self.invoice_line_ids:
                date_life.write({'lot_exp': exp_dates[c]})
                c=c+1
        """
                
    """
    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        logger.info('******************************************CREATE DE ACCOUNT*****************************')
        logger.info(self)
        logger.info(res)
        for lines in res.invoice_line_ids:
            logger.info('******************************************LOT ID*****************************')
            logger.info(lines.lot_id)
            line = lines.lot_id.replace("\n","")
            line = line.split(",")
            line_exp = lines.life_date.replace("\n","")
            line_exp = line_exp.split(",")
            logger.info('******************************************TAMAÑO LINEAS*****************************')
            logger.info(len(line_exp))
            logger.info(len(line))
            
            
            if len(line)>=2:
                for lot in line:
                    for lot_exp in line_exp:
                        if str(lines.quantity) in lot:
                            logger.info('******************************************LOT ID PASA*****************************')
                            logger.info(lot)
                            lot=str(lot)
                            logger.info(lot)
                            lot=lot.split(" ")
                            logger.info(lot)
                            lines.write({'lot_segment': lot[0] })
            else:
                lines.write({'lot_segment': line[0]})

        return res
    """
    """
    @api.depends('date','write_date')
    def _compute_lot_id(self):
        for lines in self.invoice_line_ids:
            logger.info('******************************************LOT ID*****************************')
            logger.info(lines.lot_id)
            line = lines.lot_id.replace("\n","")
            line = line.split(",")
            logger.info(line)
            logger.info(len(line))
            if len(line)>=2:
                for lot in line:
                    if str(lines.quantity) in lot:
                        logger.info('******************************************LOT ID PASA*****************************')
                        logger.info(lot)
                        lot=str(lot)
                        logger.info(lot)
                        lot=lot.split(" ")
                        logger.info(lot)
                        lines.write({'lot_segment': lot[0] })
            else:
                lines.write({'lot_segment': line[0]})
    """
                    
    
    @api.onchange('partner_shipping_id')
    def _compute_partner_delivery_zip_shipping(self):
        for record in self:
            if record.partner_shipping_id:
                if record.partner_shipping_id.zip_id:
                    record.zip_shipping_id = record.partner_shipping_id.zip_id.id
                    logger.error('************hellos_2__2/08/2021**********')
                else:
                    record.zip_shipping_id = False
            else:
                record.zip_shipping_id = False
        return
    
    @api.onchange('partner_shipping_id')
    def _compute_partner_delivery_adress_shipping(self):
        for record in self:
            if record.partner_shipping_id:
                if record.partner_shipping_id.street:
                    record.delivery_adress_shipping = record.partner_shipping_id.street
                else:
                    record.delivery_adress_shipping = False
            else:
                record.delivery_adress_shipping = False
        return
    

    def _get_invoiced_lot_values(self):
        res = super(AccountMove, self)._get_invoiced_lot_values()
        for i in res:
            obje_lot = self.env['stock.production.lot'].search([('name','=', i['lot_name'])])
            logger.error('Hello everyone test 22/01/2021')
            logger.error(res)
            if len(obje_lot)>1:
                #raise ValidationError('Error')
                logger.error('Hello everyone test 22/01/2021 one')
                logger.error(obje_lot[0].use_date)
                i['use_date'] = obje_lot[0].use_date
            else:
                logger.error('Hello everyone test 22/01/2021 two')
                logger.error(obje_lot[0].use_date)
                i['use_date'] = obje_lot[0].use_date
        #lot_values = i
        logger.error('Hello everyone test 20')
        logger.error(res)
        return res

    
    
    @api.onchange('invoice_origin')
    def _compute_method_la_fe_id(self):
        for record in self:
            if record.invoice_origin:
                logger.error(record.invoice_origin)
                if len(record.invoice_origin)> 15:
                    logger.error('************Errorone***********')
                    list_a = []
                    str_one = ""
                    count = 0
                    for i in record.invoice_origin:
                        list_a.append(i)
                        str_one = str_one + i
                        count = count +1
                        if count == 15:
                            break
                    ab = str(list_a)
                    logger.error(ab)
                    logger.error(str_one)
                else:
                    str_one = record.invoice_origin   
                logger.error('************Errotwo***********')

                logger.error(str_one)
                sale_obj = self.env['sale.order'].search([('name','=',str_one)])
                logger.error('******helloVale********')
                logger.error(sale_obj)
                record.method_la_fe_id = sale_obj.method_la_fe_id.id
            else:
                record.method_la_fe_id = False

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    #new_expiration_date = fields.Date('Fecha de Vencimiento')
    x_cum = fields.Char('Código CUM', compute='_calculate_fields_product')
    x_invima = fields.Char('Código Invima', compute='_calculate_fields_product')
    x_atc = fields.Char('Código ATC', compute='_calculate_fields_product')
    removal_date = fields.Date('Fecha de vencimiento')
    lot_segment = fields.Char('Lote')
    lot_exp = fields.Char('Fecha Vencimiento')
    

    def _sale_can_be_reinvoice(self):
        self.ensure_one()
        return not self.is_anglo_saxon_line and super(AccountMoveLineInherit, self)._sale_can_be_reinvoice()


    def _stock_account_get_anglo_saxon_price_unit(self):
        self.ensure_one()
        price_unit = super(AccountMoveLineInherit, self)._stock_account_get_anglo_saxon_price_unit()

        so_line = self.sale_line_ids and self.sale_line_ids[-1] or False
        if so_line:
            qty_to_invoice = self.product_uom_id._compute_quantity(self.quantity, self.product_id.uom_id)
            qty_invoiced = sum([x.product_uom_id._compute_quantity(x.quantity, x.product_id.uom_id) for x in so_line.invoice_lines if x.move_id.state == 'posted'])
            average_price_unit = self.product_id._compute_average_price(qty_invoiced, qty_to_invoice, so_line.move_ids)

            price_unit = average_price_unit or price_unit
            price_unit = self.product_id.uom_id._compute_price(price_unit, self.product_uom_id)
        return price_unit

    @api.depends('product_id')
    def _calculate_fields_product(self):
        for record in self: 
            if record.product_id:
                record.x_cum = record.product_id.x_cum or ''
                record.x_invima = record.product_id.x_invima or ''
                record.x_atc = record.product_id.x_atc or ''
            else:
                record.x_cum = False
                record.x_invima = False
                record.x_atc = False
            
