import Connector
import sqlalchemy

from sqlalchemy import Table, Column, MetaData, types as sqlTypes, sql

class SqlAlchemyConnector(Connector.Connector):
    def __init__(self,db):
        self.meta = MetaData();
        self.meta.bind = sqlalchemy.create_engine(db);
	self.meta.reflect();

    def selectRecords(self,name):
        self.recordTable = Table(name,self.meta);

    def selectResults(self,name):
        self.resultTable = Table(name,self.meta);

    def clearRecords(self):
	self.recordTable.drop();

    def clearResults(self):
	self.resultTable.drop();

    def getRecordCount(self):
        return self.getRowCount(self.recordTable);

    def getResultCount(self):
        return self.getRowCount(self.resultTable);

    def saveRecord(self,recordId,record):
        self.insertRow(self.recordTable,recordId,record);

    def loadRecord(self,recordId):
        return self.selectRow(self.recordTable,recordId);

    def saveResult(self,recordId,result):
        self.insertRow(self.resultTable,recordId,result);

    def loadResult(self,recordId):
        return self.selectRow(self.resultTable,recordId);

    def open(self):
        pass

    def close(self):
        pass

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
        result = table.select([sql.func.count(table.c._id)]).execute();
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
