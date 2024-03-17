Results are stored in results/

To reproduce:
```
docker run --rm -d --name cassandra -v $(pwd)/cassandra.yaml:/etc/cassandra/cassandra.yaml  --hostname cassandra --network cassandra -e CASSANDRA_BROADCAST_ADDRESS=127.0.0.2 -p 9042:9042 -p 7000:7000 cassandra
```

```
docker run --network cassandra -it -v $(pwd)/scripts:/scripts/ cassandra:latest /opt/cassandra/bin/cqlsh cassandra 9042 --cqlversion='3.4.6' -f /scripts/create_namespace_and_upload_data.cql
```

```
docker build -f docker/Dockerfile -t cassandra_run .
```

```
docker run -v $(pwd)/scripts:/fldr --network cassandra cassandra_run
```