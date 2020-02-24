# safetynet

## Creating the stack
Build and deploy all containers: ```docker-compose up --scale redis=6 --scale app=2```

Destroy everything after testing: ```docker-compose down --rmi all```

## Running tests
Execute unit tests: ```docker exec -it safetynet_app_1 pytest /safetynet```

## Redis
### Creating a distributed cluster
I followed the official guide from Redis Labs here: https://redis.io/topics/cluster-tutorial. They recommend a minimum of 3 master nodes. Each master node has a single replica for a total of 6 cluster nodes.

Additional kernel parameters that should be tuned on the VM:
* ```echo 1 > /proc/sys/vm/overcommit_memory```
* ```echo never > /sys/kernel/mm/transparent_hugepage/enabled```
