class table_op:
    def __init__(self):
        self.tables = {}

    def create_table(self,table_id):
        self.tables[str(table_id)] = {'seats': [0, 0, 0, 0]}
        #return self.tables

    def get_tables(self):
        #for i in len(self.tables):
        return self.tables

    def get_empty_tables(self):
        for i in self.tables.keys():
            print i[1]
