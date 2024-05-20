#!/bin/sh

echo "Initializing replica set..."

# Wait for MongoDB to be ready
until mongosh --host mongo1:27017 --eval "print(\"waited for connection\")" >/dev/null 2>&1; do
  echo "Waiting for MongoDB to be ready..."
  sleep 2
done

echo "MongoDB is ready. Proceeding with replica set initialization..."

# Initialize the replica set
mongosh --host mongo1:27017 <<EOF
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

if [ $? -eq 0 ]; then
  echo "Replica set initialized successfully."
else
  echo "Failed to initialize the replica set."
  exit 1
fi

mongosh --host mongo1:27017 <<EOF
rs.status()
EOF