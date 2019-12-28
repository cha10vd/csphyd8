import sqlite3

class Datastore():
    _SCHEMA = {
        'metadata': """
            CREATE TABLE IF NOT EXISTS metadata (
                target_void_vol INT,
                molecule STRING,
                comments STRING
        );""",
        'expanded': """
            CREATE TABLE IF NOT EXISTS expanded (
                csp_key INT,
                expansion FLOAT,
                res STRING,
                PRIMARY KEY (csp_key)
        );""",
        "inserted": """
            CREATE TABLE IF NOT EXISTS inserted (
                csp_key INT,
                rng_key INT,
                res STRING,
                PRIMARY KEY (csp_key, rng_key),
                FOREIGN KEY (csp_key) REFERENCES expanded(csp_key)
        );""",
        "reoptimized": """
            CREATE TABLE IF NOT EXISTS reoptimized (
                csp_key INT,
                rng_key INT,
                res STRING,
                fort12 STRING,
                cell_volume FLOAT,
                lattice_energy FLOAT,
                density FLOAT CHECK (density > 0),
                PRIMARY KEY (csp_key, rng_key),
                FOREIGN KEY (csp_key, rng_key) REFERENCES inserted (csp_key, rng_key)
        );"""
        }

    def __init__(self, fname, connect=True):
        self.filename = None
        self.connection = None
        self.cursor = None
        self.table_names = set()

        if connect:
            self.connect()
            self.load_table_names()

    @property
    def connected(self):
        return self.connection is not None

    def connect(self):

        if self.connected:
            return self.cursor

        conn = sqlite3.connect(self.filename)
        conn.execute("PRAGMA journal_mode=WAL")
        self.connection = conn
        return  self.connection.cursor()

    def commit(self):
        if self.connected:
            self.connection.commit()

    def table_exists(self, table_name):
        return table_name in self.table_names

    def get_table_names(self):
        self.cursor.execute('SELECT name FROM sqlite_master where \
                            type="table"')
        self.table_names = {row[0] for row in cursor.fetchall()}

    def create_tables(self):
        for table_name, schema in self._SCHEMA.items():
            self.cursor.execute(schema)
        self.load_table_names()

    def disconnect(self):
        if self.connected:
            self.connection.close()
        self.cursor = None
        self.connection = None

    def add_rows(self, table_name, rows, commit=True):
        assert isinstance(rows, list)
        assert len(row) > 0
        assert table_name in self.table_names

        cur = self.connect()
        placeholders = ','.join('?' for _ in range(len(rows[0])))
        statement = 'INSERT OR REPLACE INTO {} VALUES ({});'.format(table_name,
                                                                   placeholders)
        cur.executemany(statement, rows)
        if commit:
            self.commit()

    def query(self, query_text, *args):
        cur = self.connect()
        return cur.execute(query_text, *args)

    def __del__(self):
        self.disconnect()
        print("connection closed")

if __name__ == '__main__':
    c = Datastore("dipica.db")
    del c
