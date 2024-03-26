# How to run 

```bash
docker run --name cassandra-1 -d -e HEAP_NEWSIZE=128M -e MAX_HEAP_SIZE=2048M cassandra:latest
docker run --name cassandra-2 -d --link cassandra-1:cassandra -e HEAP_NEWSIZE=128M -e MAX_HEAP_SIZE=2048M cassandra:latest
docker run --name cassandra-3 -v $(pwd):/scripts/ -d --link cassandra-1:cassandra -e HEAP_NEWSIZE=128M -e MAX_HEAP_SIZE=2048M cassandra:latest
```

# Commands used
For result check folder results for screenshots.

## Task 2
```bash
docker exec -it cassandra-1 nodetool status
```

## Task 3
```bash
docker exec -it cassandra-1 bash -c 'cqlsh'
CREATE KEYSPACE cassandra_repl1 WITH replication = {'class':'SimpleStrategy' , 'replication_factor' : 1};
CREATE KEYSPACE cassandra_repl2 WITH replication = {'class':'SimpleStrategy' , 'replication_factor' : 2};
CREATE KEYSPACE cassandra_repl3 WITH replication = {'class':'SimpleStrategy' , 'replication_factor' : 3};
```

## Task 4
```bash
CREATE TABLE cassandra_repl1.employee ( emp_id int PRIMARY KEY, name text, city text );
CREATE TABLE cassandra_repl2.employee ( emp_id int PRIMARY KEY, name text, city text );
CREATE TABLE cassandra_repl3.employee ( emp_id int PRIMARY KEY, name text, city text );
```

## Task 5
```bash
docker exec -it cassandra-1 bash -c 'cqlsh'
INSERT INTO cassandra_repl1.employee (emp_id , name , city ) VALUES  (1, 'John' , 'New York' ) ;
select * from cassandra_repl1.employee;

docker exec -it cassandra-2 bash -c 'cqlsh'
select * from cassandra_repl1.employee;
INSERT INTO cassandra_repl1.employee (emp_id , name , city ) VALUES  (2, 'Jack' , 'New Amsterdam' ) ;

docker exec -it cassandra-3 bash -c 'cqlsh'
select * from cassandra_repl1.employee;
```

## Task 6
```bash
docker exec -it cassandra-3 bash -c 'cqlsh'

COPY cassandra_repl1.employee(emp_id, name, city) FROM '/scripts/employees.csv' WITH DELIMITER=',' AND HEADER = true;
COPY cassandra_repl2.employee(emp_id, name, city) FROM '/scripts/employees.csv' WITH DELIMITER=',' AND HEADER = true;
COPY cassandra_repl3.employee(emp_id, name, city) FROM '/scripts/employees.csv' WITH DELIMITER=',' AND HEADER = true;

docker exec -it cassandra-1 nodetool status
```

## Task 7
Refer to script task7.sh

## Task 8
Reading works for replication factor 2 and 3 but fails for 1.
```bash
select * from cassandra_repl1.employee;
select * from cassandra_repl2.employee LIMT 10;
 select * from cassandra_repl2.employee LIMIT 10;
```
Writing works for each replication factor
```bash
INSERT INTO cassandra_repl2.employee (emp_id , name , city ) VALUES (50, 'Mary', 'Kyiv');
INSERT INTO cassandra_repl1.employee (emp_id , name , city ) VALUES (50, 'Mary', 'Kyiv');
INSERT INTO cassandra_repl3.employee (emp_id , name , city ) VALUES (50, 'Mary', 'Kyiv');
```

## Task 9
```bash
docker exec -it cassandra-1 nodetool disablegossip
docker exec -it cassandra-1 nodetool disablehandoff
docker exec -it cassandra-2 nodetool disablegossip
docker exec -it cassandra-2 nodetool disablehandoff
docker exec -it cassandra-3 nodetool disablegossip
docker exec -it cassandra-3 nodetool disablehandoff
```

## Task 10-11
```bash
docker exec -it cassandra-1 nodetool enablegossip
docker exec -it cassandra-1 nodetool enablehandoff
....
```
At the end data it seems that data the last node that got connected was chosen.

## Task 12
Works with connected cluster and doesn't with disconnected
