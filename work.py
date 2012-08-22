import pickle

def work(fileName):
    f = open(fileName,'rb');
    connector = pickle.load(f);
    records = pickle.load(f);
    mapper = pickle.load(f);
    f.close();

    for recordId in records:
        loaded = False;
        while not loaded:
            try:
                connector.open();
                record = connector.loadRecord(recordId);
                connector.close();
            except Exception as e:
                print('Failed to load record: '+str(recordId));
                print(e);
                print('retrying...');
            else:
                loaded = True;

        try:
            result = mapper.map(record);
        except Exception as e:
            print('Failed to map record: '+str(recordId));
            print(e);
            continue;

        saved = False;
        while not saved:
            try:
                connector.open();
                connector.saveResult(recordId,result);
                connector.close();
            except Exception as e:
                print('Failed to save result: '+str(recordId));
                print(e);
                print('retrying...');
            else:
                saved = True;


if __name__ == '__main__':
    import sys;
    work(sys.argv[1]);
 
