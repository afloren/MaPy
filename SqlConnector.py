class SqlConnector:
    def __init__(self,db,dbName,recordTable,resultTable,Record,Result):
        self.db = db;
        self.dbName = dbName;
        self.recordTable = recordTable;
        self.resultTable = resultTable;
        self.Record = Record;
        self.Result = Result;
        self.open();
        if not self.tableExists(self.recordTable):
            self.createTable(self.recordTable,self.Record);
        if not self.tableExists(self.resultTable):
            self.createTable(self.resultTable,self.Result,self.recordTable);
        self.close();

    def open(self):
        self.conn = self.db.connect(self.dbName);
        self.c = self.conn.cursor();
        self._isOpen = True;

    def close(self):
        self.conn.commit();
        self.conn.close();
        self._isOpen = False;

    def clearRecords(self):
        self.dropTable(self.recordTable);
        self.createTable(self.recordTable,self.Record);

    def clearResults(self):
        self.dropTable(self.resultTable);
        self.createTable(self.resultTable,self.Result,self.recordTable);

    def clear(self):
        self.clearRecords();
        self.clearResults();

    def tableExists(self,table):
        assert(self._isOpen);
        cmd = 'select name from sqlite_master where type=\'table\' and name=\'{}\'';
        self.c.execute(cmd.format(table));
        return False if self.c.fetchone() is None else True;

    def createTable(self,table,row,ref=None):
        assert(self._isOpen);
        types = [k+' '+getSqlType(row.__dict__[k]) for k in row.__dict__ if not k[0] is '_'];
        typeStr = reduce(lambda t1,t2: t1+', '+t2,types);
        if ref is None:
            cmd = 'create table {} (id integer primary key, {})';
            self.c.execute(cmd.format(table,typeStr));
        else:
            cmd = 'create table {} (id integer primary key, rid integer references {}, {})'
            self.c.execute(cmd.format(table,ref,typeStr));

    def dropTable(self,table):
        assert(self._isOpen);
        cmd = 'drop table {}';
        self.c.execute(cmd.format(table));

    def insertRow(self,table,row,uid,ref=None,refUid=0):
        assert(self._isOpen);
        keys = [k for k in row.__dict__ if not k[0] is '_'];
        keyStr = reduce(lambda t1,t2: t1+', '+t2,keys);
        values = [row.__dict__[k] for k in keys];
        values = ['\''+v+'\'' if getSqlType(v) is 'text' else str(v) for v in values];
        valueStr = reduce(lambda v1,v2: v1+', '+v2,values);
        cmd = 'insert into {} ({}) values ({})';
        self.c.execute(cmd.format(table,keyStr,valueStr));

    def selectRow(self,table,Row,uid):
        assert(self._isOpen);
        
    def saveRecord(self,recordId,record):
        assert(self._isOpen);
        keys = [k for k in self.Record.__dict__ if not k[0] is '_'];
        keyStr = reduce(lambda t1,t2: t1+', '+t2,keys);
        values = [record.__dict__[k] for k in keys];
        values = ['\''+v+'\'' if getSqlType(v) is 'text' else str(v) for v in values];
        valueStr = reduce(lambda v1,v2: v1+', '+v2,values);
        cmd = 'insert into {} (id, {}) values ({}, {})';
        self.c.execute(cmd.format(self.recordTable,keyStr,recordId,valueStr));        

    def loadRecord(self,recordId):
        assert(self._isOpen);
        keys = [k for k in self.Record.__dict__ if not k[0] is '_'];
        keyStr = reduce(lambda t1,t2: t1+', '+t2,keys);
        cmd = 'select {} from {} where id={}';
        self.c.execute(cmd.format(keyStr,self.recordTable,recordId));
        row = self.c.fetchone();
        record = self.Record();
        for i,key in enumerate(keys):
            record.__dict__[key] = row[i];
        return record;

    def saveResult(self,recordId,result):
        assert(self._isOpen);
        keys = [k for k in self.Result.__dict__ if not k[0] is '_']
        keyStr = reduce(lambda k1,k2: k1+', '+k2,keys);
        values = [result.__dict__[k] for k in keys];
        values = ['\''+v+'\'' if getSqlType(v) is 'text' else str(v) for v in values];
        valueStr = reduce(lambda v1,v2: v1+', '+v2,values);
        cmd = 'insert into {} (rid, {}) values ({}, {})';
        self.c.execute(cmd.format(self.resultTable,keyStr,recordId,valueStr));

class Database:
    def __init__(self,dbModule):
        self.connect = dbModule.connect;
        self.apilevel = dbModule.apilevel;
        self.threadsafety = dbModule.threadsafety;
        self.paramstyle = dbModule.paramstyle;

def getSqlType(data):
    if data is int or isinstance(data,int):
        return 'integer';
    if data is long or isinstance(data,long):
        return 'integer';
    if data is float or isinstance(data,float):
        return 'real';
    if data is str or isinstance(data,str):
        return 'text';
    if data is unicode or isinstance(data,unicode):
        return 'text';
    if data is buffer or isinstance(data,buffer):
        return 'blob';
    return 'null'; 
