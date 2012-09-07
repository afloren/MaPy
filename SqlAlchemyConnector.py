import Connector
import sqlalchemy

from sqlalchemy import Table, Column, MetaData, types as sqlTypes, sql

class SqlAlchemyConnector(Connector.Connector):
    def __init__(self,db):
        self.meta = MetaData();
        self.meta.bind = sqlalchemy.create_engine(db,echo=True);
	self.meta.reflect();

    def clear(self,name):
        table = Table(name,self.meta);
        table.drop(checkfirst=True);

    def setItem(self,name,index,item):
        table = Table(name,self.meta);
        self.insertRow(table,index,item);

    def getItem(self,name,index):
        table = Table(name,self.meta);
        return self.selectRow(table,index);

    def length(self,name):
        table = Table(name,self.meta);
	return self.getRowCount(table);

    def insertRow(self,table,uid,row):
        keys = [k for k in row.__dict__ if not k[0] is '_'];
        values = [row.__dict__[k] for k in keys];
        types = [getSqlAlchemyType(v) for v in values];
        if table.exists():            
            #check if row object matches table
            assert(all([type(table.c[k].type) is t for k,t in zip(keys,types) if k in table.c]));
        else:
            #initialize table using row object
            table.append_column(Column('_id',sqlTypes.Integer,primary_key=True));
            cols = [Column(k,t) for k,t in zip(keys,types)];
            map(table.append_column,cols);
            table.create();
        table.insert().execute(_id=uid,**dict(zip(keys,values)));

    def selectRow(self,table,uid):
        assert(table.exists());
        result = sql.select([table],table.c._id==uid).execute();
        row = result.fetchone();
        return Row(table.c,row);               
        
    def getRowCount(self,table):
        result = sql.select([sql.func.count(table.c._id)]).execute();
        row = result.fetchone();	
        return row[0];

class Row:
    def __init__(self,columns,row):
        for c in columns:
            self.__dict__[c.name] = row[c];

def getSqlAlchemyType(data):
    if data is int or isinstance(data,int):
        return sqlTypes.Integer;
    if data is long or isinstance(data,long):
        return sqlTypes.Integer;
    if data is float or isinstance(data,float):
        return sqlTypes.Float;
    if data is str or isinstance(data,str):
        return sqlTypes.String;
    if data is unicode or isinstance(data,unicode):
        return sqlTypes.Unicode;
    if data is buffer or isinstance(data,buffer):
        return sqlTypes.LargeBinary;
    return sqlTypes.PickleType;#just pickle everything else
