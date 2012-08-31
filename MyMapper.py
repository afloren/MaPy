import Mapper

class Record:
    pigs = int;
    chickens = int;
    cows = int;
    fish = str;

class Result:
    fucks = int;

class MyMapper(Mapper.Mapper):      
    def map(self,record):
        result = Result();
        result.fucks = record.pigs;
        return result;
