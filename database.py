import sqlite3
import pandas as pd


class Database:
    """
    Database class that sits on top of SQLite3 that will handle data storage, import, and export.
    """

    def __init__(self):
        self.db_name = "database.db"
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.tables = [x[0] for x in self.c.execute(
            "select name from sqlite_master where type='table'").fetchall()]

    def create_table(self, table_name):
        table_name = table_name.lower()
        # create table with three columns: native = user's native language, target = language to be learned, difficulty = difficulty for user to recall target from memory
        if table_name not in self.tables:
            self.c.execute(
                f"create table if not exists {table_name} (native text,target text,difficulty integer)")
            self.tables.append(table_name)

    def import_data_from_csv(self, table_name, file_name):
        if file_name[-3:] == 'csv':
            # extract data from csv file and check for duplicates in database
            data_from_csv = pd.read_csv(file_name)
            data_in_db = pd.DataFrame(self.c.execute(
                f"select * from {table_name}").fetchall(), columns=['native', 'target', 'difficulty'])
            df = pd.merge(data_from_csv, data_in_db, indicator=True, how="outer").query(
                '_merge=="left_only"').drop('_merge', axis=1)
            self.c.executemany(
                f"insert into {table_name} values (?,?,?)", df.itertuples(index=False))
            self.conn.commit()

    def get_data_from_table(self, table_name):
        data = self.c.execute(f"select * from {table_name}").fetchall()
        return data


if __name__ == "__main__":
    pass
