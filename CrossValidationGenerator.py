import Generator
import operator
import random

class Split():
    pass

class CrossValidationGenerator(Generator.Generator):
    def __init__(self,K):
        self.K = K;
        pass

    def generate(self,input,output):
        s = range(input.length())
        random.shuffle(s)
        p = partition(s,self.K)
        output.clear()
        for id,set in enumerate(p):
            t = [s for s in p if s != set];
            split = Split();
            split.training = reduce(operator.add,t);
            split.validation = set;
            output.setItem(id,split);
        return self.K;

def partition(lst,n):
    q, r = divmod(len(lst),n);
    indices = [q*i + min(i,r) for i in xrnage(n+1)];
    return [lst[indices[i]:indices[i+1]] for i in xrnage(n)];
                               
