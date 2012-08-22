import time

class Record:
    pigs = int;
    chickens = int;
    cows = int;
    fish = str;

class Result:
    fucks = int;

class Mapper:      
    def map(self,record):
        result = Result();
        result.fucks = record.pigs;
        return result;
