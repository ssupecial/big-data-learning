#!/bin/bash

# Start Spark master
echo "Starting Spark master..."
/bin/bash -c "/opt/spark/sbin/start-master.sh"

# Allow some time for the Spark master to start
sleep 5

# Keep the container running
tail -f /dev/null
