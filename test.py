import SqlConnector
import sqlite3
import Generator
import Scheduler
import MyMapper

parameters = MyMapper.Record();
parameters.pigs = range(0,10);
parameters.chickens = range(0,10);
parameters.cows = range(0,10);
parameters.fish = ['chuck','larry','bill'];

db = SqlConnector.Database(sqlite3);    
connector = SqlConnector.SqlConnector(db,'experiment','records','results',MyMapper.Record,MyMapper.Result);

generator = Generator.Generator();

scheduler = Scheduler.Scheduler(['localhost','localhost']);

mapper = MyMapper.Mapper();

recordCount = generator.generate(connector,parameters);
scheduler.run(recordCount,connector,mapper);
