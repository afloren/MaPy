import ParameterGenerator
import Mapper
import site_config

class Record:
    pigs = int;
    chickens = int;
    cows = int;
    fish = str;

class Result:
    fucks = int;

parameters = Record();
parameters.pigs = range(0,10);
parameters.chickens = range(0,10);
parameters.cows = range(0,10);
parameters.fish = ['chuck','larry','bill'];
generator = ParameterGenerator.ParameterGenerator(parameters);

class MyMapper(Mapper.Mapper):      
    def map(self,record):
        result = Result();
        result.fucks = record.pigs;
        return (result,);
mapper = MyMapper();

records = site_config.connector.getList('records');
results = site_config.connector.getList('results');

#generator.generate(None,records);
site_config.scheduler.run(site_config.worker,mapper.map,records,results);



