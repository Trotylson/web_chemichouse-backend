import backend.libs.db_logic as base


class Tables:
    def __init__(self):
        pass

# TABLES CREATOR
        self._product = base.Db_controller(
            table_name='Products',
            db_path='./database/warehouse.db',
            columns=[
                'reference TEXT PRIMARY KEY NOT NULL',
                'company_id INT',
                'name TEXT',
                'code TEXT SECONDARY KEY',
                'stack REAL',
                'stack_min REAL',
                'price REAL',
                'last_move TEXT'
            ]
        )
        self._ordered = base.Db_controller(
            table_name='Ordered',
            db_path='./database/warehouse.db',
            columns=[
                'reference TEXT PRIMARY KEY NOT NULL',
                'company_id INT',
                'name TEXT',
                'code TEXT SECONDARY KEY',
                'total_ordered REAL',
                'payment_sum REAL',
                'last_order TEXT',
                'order_id REAL'
            ]
        )
        self._companies = base.Db_controller(
            table_name='Companies',
            db_path='./database/warehouse.db',
            columns=[
                'name TEXT PRIMARY KEY NOT NULL'
            ]
        )


# JSONIFY DATA
    # OK


    def comply_for_product_table_schema(self, packets=[]):
        data = []
        for index in packets:
            packet = {
                'reference': index[0],
                'company_id': index[1],
                'name': index[2],
                'code': index[3],
                'stack': index[4],
                'stack_min': index[5],
                'price': index[6],
                'last_move': index[7]
            }
            data.append(packet)
        return data

    # OK
    def comply_for_companies_table_schema(self, packets=[]):
        data = []
        for index in packets:
            packet = {
                'id': index[1],
                'name': index[0]
            }
            data.append(packet)
        return data

# CHECK COMPLIANCE
