import pickle

def work(fileName):
    f = open(fileName,'rb');
    worker = pickle.load(f);
    connector = pickle.load(f);
    records = pickle.load(f);
    mapper = pickle.load(f);
    f.close();

    worker.work(connector,records,mapper);

if __name__ == '__main__':
    import sys;
    work(sys.argv[1]);
 
