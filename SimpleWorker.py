import Worker

class SimpleWorker(Worker.Worker):
    def work(self,func,inputLst,outputLst,indices):	
        for index in indices:
            try:
                records = [inputLst.getItem(i) for i in index[0]]
            except Exception as e:
                print('Failed to load record: '+str(index));
                print(e);

            try:
                results = func(*records);
            except Exception as e:
                print('Failed to map record: '+str(index));
                print(e);

            try:
                for idx,i in enumerate(index[1]):
                    print(idx);
                    print(i);
                    outputLst.setItem(i,results[idx])
            except Exception as e:
                print('Failed to save result: '+str(index));
                print(e);
