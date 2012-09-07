import pickle

def work(fileName):
    f = open(fileName,'rb');
    worker = pickle.load(f);
    func = pickle.load(f);
    inputLst = pickle.load(f);
    outputLst = pickle.load(f);
    indices = pickle.load(f);
    f.close();

    worker.work(func,inputLst,outputLst,indices);

if __name__ == '__main__':
    import sys;
    work(sys.argv[1]);
 
