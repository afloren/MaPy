import Connector

class SqlConnector(Connector.Connector):

    def selectRecords(self,name):
        self.recordTable = name;
        self.open();
        if not self.tableExists(self.recordTable):
            self.createTable(self.recordTable);
        self.close();

    def selectResults(self,name):
        self.resultTable = name;
        self.open();
        if not self.tableExists(self.resultTable):
            self.createTable(self.resultTable);
        self.close();

    def clearRecords(self):
        self.dropTable(self.recordTable);
        self.createTable(self.recordTable,self.Record);

    def clearResults(self):
        self.dropTable(self.resultTable);
        self.createTable(self.resultTable,self.Result);

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
        raise NotImplementedError('SqlConnector must implement open');

    def close(self):
        raise NotImplementedError('SqlConnector must implement close');

    def tableExists(self,table):
        raise NotImplementedError('SqlConnector must implement tableExists');

    def createTable(self,table):
        raise NotImplementedError('SqlConnector must implement createTable');

    def dropTable(self,table):
        raise NotImplementedError('SqlConnector must implement dropTable');

    def insertRow(self,table,uid,row):
        raise NotImplementedError('SqlConnector must implement insertRow');

    def selectRow(self,table,uid):
        raise NotImplementedError('SqlConnector must implement selectRow');
        
    def getRowCount(self,table):
        raise NotImplementedError('SqlConnector must implement getRowCount');

