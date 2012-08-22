import os
import ssh
import pickle

class Scheduler:
    def __init__(self,hostList):
        self.hostList = hostList;

    def partition(self,recordCount):
        partitions = [];
        for node in xrange(len(self.hostList)):
            partitions.append(range(node,recordCount,len(self.hostList)));
        return partitions
    
    def run(self,recordCount,connector,mapper):
        partitions = self.partition(recordCount);
        for i,p in enumerate(partitions):
            jobName = 'job'+str(i)+'.pkl';
            f = open(jobName,'wb');
            pickle.dump(connector,f,2);
            pickle.dump(p,f,2);
            pickle.dump(mapper,f,2);
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
