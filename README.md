# safetynet

## Creating the stack
Build and deploy all containers: ```docker-compose up --scale redis=6 --scale app=2```

Bootstrap Redis cluster with test data: ```./bootstrap.sh```

Destroy everything after testing: ```docker-compose down --rmi all```

## Running tests
Execute unit tests: ```docker exec -it safetynet_app_1 pytest /safetynet```

Test it in browser: ```http://localhost:8080/urlinfo/1/abc.example.com:2000/bad/wolf```

Sample output:
```
http://localhost:8080/urlinfo/1/abc.example.com:2000/bad/wolf
---
{
  "status": "malware|adware",
  "url": "abc.example.com:2000/bad/wolf"
}
```

## Backend
### Creating a distributed Redis cluster
I followed the official guide from Redis Labs here: https://redis.io/topics/cluster-tutorial. They recommend a minimum of 3 master nodes. Each master node has a single replica for a total of 6 cluster nodes.

Additional kernel parameters that should be tuned on the VM:
* ```echo 1 > /proc/sys/vm/overcommit_memory```
* ```echo never > /sys/kernel/mm/transparent_hugepage/enabled```

## Load Balancing
### Distributing work across multiple instances
I configured NGINX to proxy incoming requests and distribute them to multiple instances of the application in a round robin fashion. As the application scales, the NGINX configuration must be updated to include the new server entries. This can be automated using templates and re-deploying the NINX container with the new configuration.
