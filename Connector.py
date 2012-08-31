
class Connector:
    def open(self):
        pass

    def close(self):
        pass

    def selectRecords(self,name,Record):
        raise NotImplementedError("Connector must implement selectRecords");

    def selectResults(self,name,Result):
        raise NotImplementedError("Connector must implement selectResults");

    def clearRecords(self):
        raise NotImplementedError("Connector must implement clearRecords");

    def clearResults(self):
        raise NotImplementedError("Connector must implement clearResults");

    def clear(self):
        self.clearRecords();
        self.clearResults();

    def saveRecord(self,recordId,record):
        raise NotImplementedError("Connector must implement saveRecord");

    def loadRecord(self,recordId):
        raise NotImplementedError("Connector must implement loadRecord");

    def getRecordCount(self):
        raise NotImplementedError("Connector must implement getRecordCount");

    def saveResult(self,recordId,result):
        raise NotImplementedError("Connector must implement saveResult");

    def loadResult(self,recordId):
        raise NotImplementedError("Connector must implement loadResult");

    def getResultCount(self):
        raise NotImplementedError("Connector must implement getResultCount");
