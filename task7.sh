for ((i=0;i<50;i++)); do
    docker exec -it cassandra-1 nodetool getendpoints cassandra_repl1 employee $i;
done