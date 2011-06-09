from sqlalchemy import create_engine, Index, MetaData
from sqlalchemy.schema import CreateIndex, CreateTable
from sqlalchemy.engine import reflection


def dump_sql(connection_string):
    engine = create_engine(connection_string)
    insp = reflection.Inspector.from_engine(engine)
    meta = MetaData()
    meta.reflect(bind=engine)
    for table_name, table_object in meta.tables.items():
        try:
            print CreateTable(table_object, bind=engine)
            for index in insp.get_indexes(table_name):
                cols = [table_object.c[col] for col in index['column_names']]
                idx = Index(index['name'], *cols)
                print CreateIndex(idx, bind=engine)
        except Exception, e:
            print e
            print "Could not print create statement for table %s" % table_name
            print repr(table_object)
