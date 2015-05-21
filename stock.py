# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _


   
#class stock_quant(osv.osv):
#    _inherit= 'stock.quant'
#    _columns = {
#	    'meter': fields.related('lot_id', 'meter', type='char', string='meter', help="meter"),
#	    'conumber': fields.related('lot_id', 'conumber', type='char', string='conumber', help="conumber"),
#	    'width': fields.related('lot_id', 'width', type='char', string='width', help="width"),
#	}

class stock_picking(osv.osv):
    _inherit= 'stock.picking'
    _columns = {
        'move_lines2': fields.one2many('stock.move2', 'picking_id', 'Sum Moves'),
#	    'conumber': fields.related('lot_id', 'conumber', type='char', string='conumber', help="conumber"),
#	    'width': fields.related('lot_id', 'width', type='char', string='width', help="width"),
	}

class stock_move2(osv.osv):
    _name = "stock.move2"
    _description = "stock move2"
    _auto = False
    _rec_name = 'picking_id'

    _columns = {
        'picking_id': fields.many2one('stock.move', 'stock picking', readonly=True),
        'product_id': fields.many2one('product.product', 'product', readonly=True),
        'product_qty': fields.float('product qty', digits=(16,2), readonly=True),
        'number': fields.integer('number', readonly=True),
        'money': fields.float('Price', digits=(16,2), readonly=True),
        'amount': fields.float('amount', digits=(16,2), readonly=True),
    }
    _order = 'picking_id desc'

    def _select(self):
        select_str = """
             SELECT c.picking_id::text || '-' || c.product_id::text || '-' || case when c.money is null  then 0 else c.money end::text AS id ,
					c.picking_id as picking_id ,
                    c.product_id as product_id,
                    sum(c.product_qty) as product_qty,
                    sum(c.number) as number,
					c.money as money,
					c.money*sum(c.product_qty) as amount
        """
        return select_str

    def _from(self):
        from_str = """
               stock_move c
        """
        return from_str

    def _group_by(self):
        group_by_str = """ GROUP BY
                c.picking_id,
                c.product_id,
				c.money
        """
        return group_by_str

    def init(self, cr):
        #self._table = stock_move2
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM  %s 
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))
