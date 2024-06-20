import xmlrpc.client
url ='https://www.odoo.com/'
db ='openerp'
login = 'alot@.com'
pwd = ''

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db,login,pwd,{})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

company_id = 14
department_id = 152

Efields = {'fields': ['user_id']}
Edomain = [[
    ("company_id", "=", company_id), 
    ("department_id", "=", department_id)]]

analyst_ids = models.execute_kw(db, uid, pwd, 'hr.employee.public', 'search', Edomain)
analysts = models.execute_kw(db, uid, pwd,'hr.employee.public', 'read',[analyst_ids],Efields)
print(analyst_ids)