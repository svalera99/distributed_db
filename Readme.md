Commands to configure cluster
```bash

mongod --replSet rs0 --port 27017 --bind_ip_all --dbpath /home/valery/mongodb/rs0-0  --oplogSize 128
mongod --replSet rs0 --port 27018 --bind_ip_all --dbpath /home/valery/mongodb/rs0-1  --oplogSize 128
mongod --replSet rs0 --port 27019 --bind_ip_all --dbpath /home/valery/mongodb/rs0-2 --oplogSize 128


mongosh --port 27017

rsconf = {
      "_id" : "rs0",
      "members" : [
          {
              "_id" : 0,
              "host" : "localhost:27017"
          },
          {
              "_id" : 1,
              "host" : "localhost:27018"
          },
          {
              "_id" : 2,
              "host" : "localhost:27019"
          }
      ]
  }
rs.config(rsconf)
rs.conf()
```