import Generator
import operator
import random

class Split():
    training = list;
    validation = list;

class CrossValidationGenerator(Generator.Generator):
    def __init__(self,K,recordName):
        self.K = K;
        self.recordName = recordName;
        pass

    def generate(self,connector):
        connector.selectRecords(self.recordName);
        recordCount = connector.getRecordCount();
        s = range(self.recordCount);
        random.shuffle(s);
        p = partition(s,self.K);
        connector.open();
        connector.clearRecords();
        for id,set in enumerate(p):
            t = [s for s in p if s != set];
            split = Split();
            split.training = reduce(operator.add,t);
            split.validation = set;
            connector.saveRecord(id,split);
        connector.close();
        return self.K;

def partition(lst,n):
    q, r = divmod(len(lst),n);
    indices = [q*i + min(i,r) for i in xrnage(n+1)];
    return [lst[indices[i]:indices[i+1]] for i in xrnage(n)];
                               
