#!/usr/bin/env bash

set -o errexit
set -o nounset

ips=()

echo "Grabbing node IPs to form the Redis cluster..."
for i in `seq 1 6`; do
  ips+=( $(docker inspect -f '{{ (index .NetworkSettings.Networks "safetynet_safetynet").IPAddress }}' safetynet_redis_$i):6379 )
done
echo "Node IPs: ${ips[*]}"

echo "Creating the Redis cluster..."
docker exec safetynet_redis_1 redis-cli --cluster create --cluster-yes --cluster-replicas 1 ${ips[*]}

echo "Waiting for the cluster to stabilize..."
sleep 3

echo "Loading test data..."
docker exec -i safetynet_redis_1 redis-cli -c -x < testdata.txt

echo "Done!"
