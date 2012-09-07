import SqlConnector
import pickle
import sqlalchemy

from sqlalchemy import Table, Column, Integer, PickleType, MetaData, sql

class PickleConnector(SqlConnector.SqlConnector):
    def __init__(self,db):
        self.meta = MetaData();
        self.meta.bind = sqlalchemy.create_engine(db);

    def open(self):
        pass

    def close(self):
        pass

    def tableExists(self,table):
        t = Table(table,self.meta);
        return t.exists();

    def createTable(self,table):
        t = Table(table,self.meta);
        t.append_column(Column('id', Integer, primary_key=True));
        t.append_column(Column('obj', PickleType));
        t.create();

    def dropTable(self,table):
        t = Table(table,self.meta);
        t.drop();

    def insertRow(self,table,uid,row):
        t = Table(table,self.meta);
        t.insert().execute(id=uid,obj=row);

    def selectRow(self,table,uid):
        t = Table(table,self.meta);
        result = sql.select([t.c.obj],t.c.id==uid).execute();
        row = result.fetchone();
        return row[0];
        
    def getRowCount(self,table):
        t = Table(table,self.meta);
        result = t.select([sql.func.count(t.c.id)]).execute();
        row = result.fetchone();
        return row[0];


