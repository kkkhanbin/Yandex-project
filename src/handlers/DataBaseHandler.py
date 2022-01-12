import sqlite3


class DataBaseHandler:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def get_connection(self) -> sqlite3.Connection:
        return self.connection

    def get_cursor(self) -> sqlite3.Cursor:
        return self.get_connection().cursor()

    def select(self, table_name: str,
               columns_names: tuple, conditions: dict) -> sqlite3.Cursor:
        cursor = self.get_cursor()

        request = f'''
            SELECT {', '.join(map(str, columns_names))} FROM {table_name}
            '''
        if conditions:
            request += f'''
            \nWHERE {' AND '.join(map(lambda item: ' = '.join(map(str, item)),
                                      conditions.items()))}
            '''

        return cursor.execute(request)

    def insert(self, table_name: str,
               columns_names: tuple, values: tuple) -> None:
        cursor = self.get_cursor()

        if columns_names:
            columns_names = f"({', '.join(map(str, columns_names))})"
        else:
            columns_names = ''

        request = f'''
        INSERT INTO {table_name}{columns_names}
        VALUES {', '.join(map(str, values))}
        '''

        cursor.execute(request)

    def update(self, table_name: str,
               values: dict, conditions: dict) -> None:
        cursor = self.get_cursor()

        request = f'''
        UPDATE {table_name}
        SET {', '.join(map(lambda item: ' = '.join(map(str, item)),
                           values.items()))}
        '''

        if conditions:
            request += f'''
            \nWHERE {' AND '.join(map(lambda item: ' = '.join(map(str, item)),
                                      conditions.items()))}
            '''

        cursor.execute(request)

    def delete(self, table_name: str,
               conditions: dict) -> None:
        cursor = self.get_cursor()

        request = f'''
        DELETE FROM {table_name}
        '''

        if conditions:
            request += f'''
            \nWHERE {' AND '.join(map(lambda item: ' = '.join(map(str, item)),
                                      conditions.items()))}
            '''

        cursor.execute(request)
