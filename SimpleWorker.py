import Worker

class SimpleWorker(Worker.Worker):
    def work(self,connector,records,mapper):
	connector.open();
        for recordId in records:
            try:
                record = connector.loadRecord(recordId);
            except Exception as e:
                print('Failed to load record: '+str(recordId));
                print(e);

            try:
                result = mapper.map(record);
            except Exception as e:
                print('Failed to map record: '+str(recordId));
                print(e);

            try:
                connector.saveResult(recordId,result);
            except Exception as e:
                print('Failed to save result: '+str(recordId));
                print(e);
        connector.close();
