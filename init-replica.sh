#!/bin/bash
echo "Waiting for MongoDB to start..."
sleep 15

echo "Initializing replica set..."
mongo --host mongo1:27017 <<EOF
rs.initiate(
  {
    _id: "mongoReplicaSet",
    members: [
      { _id: 0, host: "mongo1:27017" },
      { _id: 1, host: "mongo2:27017" },
      { _id: 2, host: "mongo3:27017" }
    ]
  }
)
EOF
