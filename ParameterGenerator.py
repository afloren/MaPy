import Generator
import operator

class Parameters:
    pass

class ParameterGenerator(Generator.Generator):
    def __init__(self,parameters):
        self.parameters = parameters;

    def generate(self,input,output):
        keys = [k for k in self.parameters.__dict__ if not k[0] is '_'];
        dims = [len(self.parameters.__dict__[k]) for k in keys];
        recordCount = reduce(operator.mul,dims);
        output.clear();
        for recordId in xrange(recordCount):
            subs = ind2sub(dims,recordId);
            record = Parameters();
            for i,k in enumerate(keys):
                record.__dict__[k] = self.parameters.__dict__[k][subs[i]];
            output.setItem(recordId,record);
        return recordCount;

def ind2sub(dims,index):
    r=[];
    for dim in dims:
        r.append(index%dim);
        index = index/dim;
    return r;
