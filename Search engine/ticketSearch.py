import xmlrpc.client
from datetime import datetime
url ='https://www.odoo.com/'
db ='openerp'
login = 'alot@odoo.com'
pwd = '98c2f9d2ee2663495089a8390cbabe750616f73e'

current_date = datetime.now()
three_years_before = current_date.replace(year=current_date.year - 3)
jan_first = three_years_before.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
jan_first_3years_ago = jan_first.strftime('%Y-%m-%d %H:%M:%S')

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db,login,pwd,{})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

Efields = {'fields': ['user_partner_id']}
Edomain = [[["department_id", "=", 152],["active", "in", [True, False]]]]
analysts = models.execute_kw(db, uid, pwd,'hr.employee.public', 'search_read',Edomain,Efields)
contact_ids = [entry['user_partner_id'][0] for entry in analysts if entry['user_partner_id']]

while True:
    try:
        searchTerm = str(input("Search Tickets for: "))
        print('Searching Ticket description......')
        Tdomain = [["&", "&","&", ("project_id", "=", 49), ("description", "ilike", searchTerm), ("user_ids", "!=", False),("create_date", ">", jan_first_3years_ago)]]
        tickets = models.execute_kw(db, uid, pwd,'project.task', 'search',Tdomain)

        print('Searching Ticket messages......')
        Mdomain = [[['model','=','project.task'],['author_id','in',contact_ids],["res_id", "not in", tickets], ["body", "ilike", searchTerm],["create_date", ">", jan_first_3years_ago]]]
        Mfields = {'fields':['res_id']}
        msg_tickets = models.execute_kw(db, uid, pwd,'mail.message', 'search_read',Mdomain,Mfields)
        msg_tickets = [item['res_id'] for item in msg_tickets]

        tickets += msg_tickets
        tickets = list(set(tickets))

        output = f'[("id", "in", {tickets})]'
        print(f'Apply this filter to get the tickets:\n=======================================\n\n{output}\n\n=======================================\n\nCtrl + C to exit')
    except KeyboardInterrupt:
        print('\n')
        break