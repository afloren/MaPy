import SqlAlchemyConnector
import SSHScheduler
import SimpleWorker

connector = SqlAlchemyConnector.SqlAlchemyConnector('sqlite:///experiment');

scheduler = SSHScheduler.SSHScheduler(['localhost']);

worker = SimpleWorker.SimpleWorker();
