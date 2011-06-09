from sqlalchemy import create_engine
from sqlalchemy.engine import reflection

engine = create_engine('sqlite:////tmp/meh.db')
insp = reflection.Inspector.from_engine(engine)
print insp.get_table_names()
