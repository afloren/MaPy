import Scheduler
import os
import ssh
import pickle

import copy_reg
import types

def reduce_method(m):
    return (getattr, (m.__self__, m.__func__.__name__))

copy_reg.pickle(types.MethodType, reduce_method)

class SSHScheduler(Scheduler.Scheduler):
    def __init__(self,hostList):
        self.hostList = hostList;

    def partition(self,recordCount):
        partitions = [];
        for node in xrange(len(self.hostList)):
            partitions.append(range(node,recordCount,len(self.hostList)));
        return partitions
    
    def run(self,worker,func,inputLst,outputLst):        
        recordCount = inputLst.length();
        print(recordCount);
        partitions = self.partition(recordCount);
        for i,part in enumerate(partitions):
            part = [((p,),(p,)) for p in part];
            #worker.work(func,inputLst,outputLst,part);
            jobName = 'job'+str(i)+'.pkl';
            f = open(jobName,'wb');
            pickle.dump(worker,f,2);
            pickle.dump(func,f,2);
            pickle.dump(inputLst,f,2);
            pickle.dump(outputLst,f,2);
            pickle.dump(part,f,2);
            f.close();
            #execute work.py for each job
            client = ssh.SSHClient();
            client.load_system_host_keys();
            client.connect(self.hostList[i]);
            #sftp = client.open_sftp();
            #sftp.chdir('work');
            #sftp.put(jobName,jobName);
            wd = os.getcwd();
            client.exec_command('cd '+wd+'; screen -d -m -L -S '+jobName+' python work.py '+jobName);
            client.close();

        return
