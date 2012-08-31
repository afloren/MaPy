import Generator
import operator

class ParameterGenerator(Generator.Generator):
    def __init__(self,parameters):
        self.parameters = parameters;

    def generate(self,connector):
        keys = [k for k in connector.Record.__dict__ if not k[0] is '_'];
        dims = [len(self.parameters.__dict__[k]) for k in keys];
        recordCount = reduce(operator.mul,dims);
        connector.open();
        connector.clearRecords();
        for recordId in xrange(recordCount):
            subs = ind2sub(dims,recordId);
            record = connector.Record();
            for i,k in enumerate(keys):
                record.__dict__[k] = self.parameters.__dict__[k][subs[i]];
            connector.saveRecord(recordId,record);
        connector.close();
        return recordCount;

def ind2sub(dims,index):
    r=[];
    for dim in dims:
        r.append(index%dim);
        index = index/dim;
    return r;
