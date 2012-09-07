
class Connector:
    def getList(self,name):	
        return List(self,name);

    def clear(self,name):
        raise NotImplementedError("Connector must implement clear");

    def setItem(self,name,index,item):
        raise NotImplementedError("Connector must implement saveItem");

    def getItem(self,name,index):
        raise NotImplementedError("Connector must implement getItem");

    def length(self,name):
        raise NotImplementedError("Connector must implement length");

class List:
    def __init__(self,connector,name):
        self.connector = connector;
        self.name = name;

    def clear(self):
        self.connector.clear(self.name);

    def setItem(self,index,item):
        self.connector.setItem(self.name,index,item);

    def getItem(self,index):
        return self.connector.getItem(self.name,index);

    def length(self):
        return self.connector.length(self.name);

    
