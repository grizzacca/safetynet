# safetynet

## Redis
### Creating a distributed cluster
Followed the official guide from Redis Labs here: https://redis.io/topics/cluster-tutorial. They recommend a minimum of 3 master nodes.

Additional kernel parameters that should be tuned on the VM:
* ```echo 1 > /proc/sys/vm/overcommit_memory```
* ```echo never > /sys/kernel/mm/transparent_hugepage/enabled```
