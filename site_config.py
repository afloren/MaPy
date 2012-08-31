import sqlite3
import SqlConnector
import SSHScheduler
import SimpleWorker

connector = SqlConnector.SqlConnector(SqlConnector.Database(sqlite3),
                                      'experiment');

scheduler = SSHScheduler.SSHScheduler(['localhost']);

worker = SimpleWorker.SimpleWorker();
