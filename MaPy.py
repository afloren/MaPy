
def go(fileName,records,results,generatorName,
       mapperName,RecordName,ResultName):
    import site_config;
    module = __import__(fileName);
    generator = module.__dict__[generatorName];
    mapper = module.__dict__[mapperName];
    Record = module.__dict__[RecordName];
    Result = module.__dict__[ResultName];
    site_config.connector.selectRecords(records,Record);
    site_config.connector.selectResults(results,Result);
    generator.generate(site_config.connector);
    site_config.scheduler.run(site_config.connector,site_config.worker,
                              mapper);

if __name__ == '__main__':
    import sys;
    go(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],
       sys.argv[5],sys.argv[6],sys.argv[7]);
    
