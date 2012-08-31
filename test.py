import sqlite3
import SqlConnector
import ParameterGenerator
import SSHScheduler
import SimpleWorker
import MyMapper

db = SqlConnector.Database(sqlite3);    
connector = SqlConnector.SqlConnector(db,'experiment')
scheduler = SSHScheduler.SSHScheduler(['localhost']);
worker = SimpleWorker.SimpleWorker();

parameters = MyMapper.Record();
parameters.pigs = range(0,10);
parameters.chickens = range(0,10);
parameters.cows = range(0,10);
parameters.fish = ['chuck','larry','bill'];
generator = ParameterGenerator.ParameterGenerator(parameters);

connector.selectRecords('records',MyMapper.Record);
connector.selectResults('results',MyMapper.Result);

mapper = MyMapper.MyMapper();

generator.generate(connector);
scheduler.run(connector,worker,mapper);
