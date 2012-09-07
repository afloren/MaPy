#this is a fake python script that shows how I would LIKE to use MaPy
import MaPy
import SomeGenerator
import SomeMapper
import SomeReducer

MaPy.Generate(SomeGenerator.SomeGenerator(),'records');
MaPy.Map(SomeMapper.SomeMapper(),'records','results');
MaPy.Reduce(SomeReducer.SomeReducer(),'results','aggregates');
#perhaps make the above behave intelligently based on first input parameter
#ie if it is a module then check if the module has a function or class of the same name
#if it is a class then try to instantiate it

import AnotherGenerator
import SomeScheduler
import SomeConnector

MaPy.Generate(AnotherGenerator,'records','records2');#generators may have an input list
MaPy.Map(SomeMapper,'records2','results2',scheduler=SomeScheduler);
#this should probably be an error because results2 probably doesn't exist on SomeConnector
MaPy.Reduce(SomeReducer,'results2','aggregates2',SomeConnector);

import AnotherScheduler
import AnotherWorker

MaPy.setScheduler(AnotherScheduler);
MaPy.setWorker(AnotherWorker);

def Mapper(record):
    result = record.x / record.y;
    return result;

MaPy.Map(Mapper,'records2','results3');
