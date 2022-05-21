from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from backend.libs.tables_controller import Tables as tables
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get('/returnCompanyName')
# def return_company_id(company_id: int):
#     company_table = tables()._companies
#     company_name = company_table.changer_value_to_value(column='name', command=f"WHERE rowid='{company_id}'")
#     print(company_name)
#     return {'name': company_name}


# => GET
@app.get('/warehouseContent')  # OK
def schow_warehouse_content():
    req = tables()
    company_table = req._companies
    table = req._product
    packet = []
    for record in table._show():
        _record = list(record)
        company_name = company_table.return_value_by_index(
            column='name', command=f"WHERE rowid={record[1]}")
        _record[1] = company_name
        packet.append(_record)
        print(_record)
    send = req.comply_for_product_table_schema(packets=packet)
    table.close()
    company_table.close()
    return send


@app.get('/searchItem')  # OK
def search_item(item: str):
    _alt = f"where company_id LIKE '%{item}%' OR name LIKE '%{item}%' OR reference LIKE '%{item}%' OR code LIKE '%{item}%'"
    req = tables()
    company_table = req._companies
    table = req._product
    packet = []
    for record in table._show(alt_command=_alt):
        _record = list(record)
        company_name = company_table.return_value_by_index(
            column='name', command=f"WHERE rowid={record[1]}")
        _record[1] = company_name
        packet.append(_record)
        print(_record)
    send = req.comply_for_product_table_schema(packets=packet)
    table.close()
    company_table.close()
    return send


@app.get('/showToOrder')  # OK
def to_order_info():
    _alt = "WHERE stack <= stack_min"
    req = tables()
    company_table = req._companies
    table = req._product
    packet = []
    for record in table._show(alt_command=_alt):
        _record = list(record)
        company_name = company_table.return_value_by_index(
            column='name', command=f"WHERE rowid={record[1]}")
        _record[1] = company_name
        packet.append(_record)
        print(_record)
    send = req.comply_for_product_table_schema(packets=packet)
    table.close()
    company_table.close()
    return send


@app.get('/showCompanies')  # OK
def schow_companies():
    req = tables()
    table = req._companies
    packet = []
    for record in table._show(column='name, rowid'):
        packet.append(record)
    send = req.comply_for_companies_table_schema(packets=packet)
    table.close()
    return send

# => POST


# @app.post('/addCompany')  # OK
# def add_company(name: str):
#     table = tables()._companies
#     status = table._insert([name])
#     table.close()
#     return status


@app.post('/addNewItem')  # OK
def add_item(reference: str, company_name: str, name: str, code: str, quantity: int, minimum: int, price: float):
    req = tables()
    table = req._product
    company_table = req._companies
    _name = company_table.return_value_by_index(
        column="rowid", command=f" WHERE name='{company_name}'")
    if _name:
        company_name = _name
    else:
        company_table._insert([company_name])
        company_name = company_table.return_value_by_index(
            column="rowid", command=f" WHERE name='{company_name}'")

    status = table._insert(
        [reference, company_name, name, code, quantity, minimum, price, datetime.today()])
    table.close()
    company_table.close()
    print(status)
    return status

# => PUT


@app.put('/moveStack')  # OK
def move_stack(signature_to_edit: str, quantity: int):
    _where = f"reference = '{signature_to_edit}'"
    _update_values = f"stack = stack+{quantity}, last_move = '{datetime.today()}'"
    table = tables()._product
    if table._show(column='reference', alt_command=f"WHERE {_where}"):
        status = table._edit(_update_values, _where)
    else:
        status = {'status': 'unsuccess!'}
    table.close()
    return status


@app.put('/editRecord')  # OK
def edit_item(signature_to_edit: str, reference: str, company_name: str, item_name: str, code: str, stack: int, stack_min: int, price: float):
    req = tables()
    table = req._product
    company_table = req._companies

    _name = company_table.return_value_by_index(
        column="rowid", command=f" WHERE name='{company_name}'")
    if _name:
        company_name = _name
    else:
        company_table._insert([company_name])
        company_name = company_table.return_value_by_index(
            column="rowid", command=f" WHERE name='{company_name}'")

    _where = f"reference='{signature_to_edit}'"
    _update_values = f"reference='{reference}', company_id={company_name}, name='{item_name}', code='{code}', stack={stack}, stack_min={stack_min}, price={price}, last_move='{datetime.today()}'"

    if table._show(column='reference', alt_command=f"WHERE {_where}"):
        status = table._edit(_update_values, _where)
    else:
        status = {'status': 'unsuccess!'}
    table.close()
    company_table.close()
    return status

# => DELETE


@app.delete('/deleteItem')  # OK
def delete_item(reference: str):
    _alt = f'WHERE reference={reference}'
    _where = f'reference={reference}'
    table = tables()._product
    if table._show(column='reference', alt_command=_alt):
        status = table._delete(_where)
    else:
        print('[!] => no reference')
        status = {'status': 'unsuccess'}
    table.close()
    return status

############# TEST AREA ###############


# @app.post('/pushOrder')
# def make_order(reference: str, company_id: int, name: str, code: str, quantity: int, price: float):
#     check = f"WHERE reference='{reference}'"
#     _alt = f"reference='{reference}'"
#     table = tables()._ordered
#     for record in table._show(alt_command=check):
#         if record[0] == reference:
#             print(f"reference {reference} exist - appending")
#             total = record[4] + quantity
#             pay = record[5] + price
#             status = table._edit(update_values=f"""
#                                  reference='{reference}',
#                                  company_id={company_id},
#                                  name='{name}',
#                                  code='{code}',
#                                  total_ordered={total},
#                                  payment_sum={pay},
#                                  last_move='{datetime.today()}',
#                                  order_id=1""",
#                                  command=_alt)
#         else:
#             print(f"reference {reference} not exist - creating")
#             print('RECORD TO ADD:', record)
#             status = table._insert([reference, company_id, name, code, quantity, price, datetime.today(), '1'])
#         table.close()
#         return status
