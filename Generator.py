import operator

class Generator:
    def generate(self,connector,parameters):
        keys = [k for k in connector.Record.__dict__ if not k[0] is '_'];
        dims = [len(parameters.__dict__[k]) for k in keys];
        recordCount = reduce(operator.mul,dims);
        connector.open();
        connector.clear();
        for recordId in xrange(recordCount):
            subs = ind2sub(dims,recordId);
            record = connector.Record();
            for i,k in enumerate(keys):
                record.__dict__[k] = parameters.__dict__[k][subs[i]];
            connector.saveRecord(recordId,record);
        connector.close();
        return recordCount;

def ind2sub(dims,index):
    r=[];
    for dim in dims:
        r.append(index%dim);
        index = index/dim;
    return r;
