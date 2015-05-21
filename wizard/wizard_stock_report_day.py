
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_stock_report_day(osv.osv_memory):

    _name = 'wizard.stock.report.day'
    _description = 'Wizard that opens the stock valuation history table'
    _columns = {
        'choose_date': fields.boolean('Choose a Particular Date'),
        'choose_attribute': fields.boolean('Choose Attributes of products'),
        'choose_company': fields.boolean('Choose a company'),
        'date': fields.datetime('Date', required=True),
        'test': fields.char('test'),
		'attribute_line_ids': fields.many2one('product.attribute.value','Attribute_1'),
        'attribute_value_1': fields.many2one('product.attribute.value','Attribute_1'),
        'attribute_value_2': fields.many2one('product.attribute.value','Attribute_2'),
        'attribute_value_3': fields.many2one('product.attribute.value','Attribute_3'),
        'attribute_value_4': fields.many2one('product.attribute.value','Attribute_4'),
		'company_id': fields.many2one('res.company','Company'),
    }

    _defaults = {
        'choose_date': False,
        'choose_attribute': False,
        'choose_company': False,
        'date': fields.datetime.now,
    }

    def open_table(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        if data['attribute_line_ids']:
            test =  data['attribute_line_ids'][1]
        else :
            test =''     
        if data['attribute_value_1']:
            value_1 =  data['attribute_value_1'][1]
        else :
            value_1 =''
        if data['attribute_value_2']:
            value_2 =  data['attribute_value_2'][1]
        else :
            value_2 =''
        if data['attribute_value_3']:
            value_3 =  data['attribute_value_3'][1]
        else :
            value_3 =''             
        if data['attribute_value_4']:
            value_4 =  data['attribute_value_4'][1]
        else :
            value_4 =''
        if data['company_id']:
            cid =  data['company_id'][1]
        else :
            cid =''                                                  
        ctx = context.copy()
        ctx['history_date'] = data['date']
        ctx['search_default_today'] = True
        #ctx['search_default_group_by_month'] = True
        
        #ctx['search_default_group_by_location'] = True
        if data['choose_company'] :
            return {
                'domain': "[('company_id.name', 'like', '" +cid + "')]",
                'name': _('Stock report at day'),
                'view_type': 'form',
                'view_mode': 'graph,tree',
                'res_model': 'stock.quant.history2',
                'type': 'ir.actions.act_window',
                'context': ctx,
			}
        else :
            return {
                'domain': "[]",
                'name': _('Stock Report At day'),
                'view_type': 'form',
                'view_mode': 'graph,tree',
                'res_model': 'stock.quant.history2',
                'type': 'ir.actions.act_window',
                'context': ctx,
            }