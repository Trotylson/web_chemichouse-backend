import sqlite3

"""
    DATABASE CONTROLLER
    author: Trotylson
    ver: 0.1
    
    tip: call Db_controller
"""

# STATIC CLASS


class Db_core:
    def __init__(self, db_path=None, table_name=None, columns=[]):

        self.db_path = db_path
        self.table_name = table_name
        self.columns = columns

        self.core = ''
        for param in self.columns:
            if param:
                param += ', '
                self.core += param
        self.core = self.core[:-2]

        try:
            open(f'{self.db_path}')
            print(f'[OK] ==> Found path {self.db_path}')
        except:
            print(f'[!] ==> Path not found - creating path {self.db_path}')

        print(
            f'[*] ==> Starting database in {self.db_path} inside:\n\nTABLE: {self.table_name} / {str(len(self.columns))} column(s)\n    ____')
        for name in self.columns:
            print('     => |-', name)
        print('\n')

        try:
            self.conn = sqlite3.connect(
                f'{self.db_path}', check_same_thread=False)
            self.db = self.conn.cursor()
            self.db.execute(
                f'''CREATE TABLE IF NOT EXISTS {self.table_name} ({self.core})''')
            self.conn.commit()
        except Exception as e:
            print(f'[!] caught error as {str(e)}')

    def close(self):
        self.conn.close()
        print('Database closed successfully!')


class Db_controller(Db_core):
    def __init__(self, db_path=None, table_name=None, columns=[]):
        self.db_path = db_path
        self.table_name = table_name
        self.columns = columns
        super().__init__(self.db_path, self.table_name, self.columns)

    # OK
    def _show(self, column='*', alt_command=''):
        items = []
        for record in self.db.execute(f"SELECT {column} FROM {self.table_name} {alt_command}"):
            items.append(record)
        # print(items)
        return items

    # OK
    def _insert(self, to_insert=[]):
        _match = ''
        _len = len(to_insert)
        for x in range(_len):
            _match += '?, '
        _match = _match[:-2]
        try:
            self.db.execute(
                f'INSERT INTO {self.table_name} VALUES({_match})', (to_insert))
            self.conn.commit()
            return {'status': 'success'}
        except Exception as e:
            print(f'[ERROR] ==> {str(e)}')
            return {'status': 'unsuccess'}

    # OK
    def _edit(self, update_values, command):
        print(
            f'UPDATE {self.table_name} SET {update_values} WHERE {command}')
        self.db.execute(
            f'UPDATE {self.table_name} SET {update_values} WHERE {command}')
        self.conn.commit()
        return {'status': 'updated'}

    # OK
    def _delete(self, command):
        self.db.execute(f'DELETE FROM {self.table_name} WHERE {command}')
        self.conn.commit()
        return {'status': 'success'}

    #########

    def return_value_by_index(self, column='*', command=''):
        for param in self.db.execute(f"SELECT {column} FROM {self.table_name} {command}"):
            return param[0]
