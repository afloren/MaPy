import SqlConnector
import sqlite3

class SqlConnector(SqlConnector.SqlConnector):
    def __init__(self,db):
        self.db = db;
	self._isOpen = False;

    def open(self):
        if not self._isOpen:
            self.conn = sqlite3.connect(self.db);
            self.c = self.conn.cursor();
            self._isOpen = True;

    def close(self):
        if self._isOpen:
            self.conn.commit();
            self.conn.close();
            self._isOpen = False;

    def tableExists(self,table):
        assert(self._isOpen);
        cmd = 'select name from sqlite_master where type=\'table\' and name=\'{}\'';
        self.c.execute(cmd.format(table));
        return False if self.c.fetchone() is None else True;

    def createTable(self,table,Row):
        assert(self._isOpen);
        types = [k+' '+getSqlType(Row.__dict__[k]) for k in Row.__dict__ if not k[0] is '_'];
        typeStr = reduce(lambda t1,t2: t1+', '+t2,types);
        cmd = 'create table {} (id integer primary key, {})';
        self.c.execute(cmd.format(table,typeStr));

    def dropTable(self,table):
        assert(self._isOpen);
        cmd = 'drop table {}';
        self.c.execute(cmd.format(table));

    def insertRow(self,table,Row,uid,row):
        #assert(self.checkTypes(Row,row));
        assert(self._isOpen);
        keys = [k for k in Row.__dict__ if not k[0] is '_'];
        keyStr = reduce(lambda t1,t2: t1+', '+t2,keys);
        values = [row.__dict__[k] for k in keys];
        values = ['\''+v+'\'' if getSqlType(v) is 'text' else str(v) for v in values];
        valueStr = reduce(lambda v1,v2: v1+', '+v2,values);
        cmd = 'insert into {} (id, {}) values ({}, {})';
        self.c.execute(cmd.format(table,keyStr,uid,valueStr));

    def selectRow(self,table,Row,uid):
        assert(self._isOpen);
        keys = [k for k in Row.__dict__ if not k[0] is '_'];
        keyStr = reduce(lambda t1,t2: t1+', '+t2,keys);
        cmd = 'select {} from {} where id={}';
        self.c.execute(cmd.format(keyStr,table,uid));
        r = self.c.fetchone();
        row = Row();
        for i,key in enumerate(keys):
            row.__dict__[key] = r[i];
        return row;
        
    def getRowCount(self,table):
        assert(self._isOpen);
        cmd = 'select count(*) from {}';
        self.c.execute(cmd.format(table));
        row = self.c.fetchone();
        return row[0];


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
