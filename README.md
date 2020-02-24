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
curl http://localhost:8080/urlinfo/1/abc.example.com:2000/bad/wolf
---
{
  "status": "malware|adware",
  "url": "abc.example.com:2000/bad/wolf"
}
```

The status field in the response body indicates whether it's safe to proceed or there's a risk of malware, and describes the type of malware associated with it.

## Project structure
### Infrastructure pieces

**Project root:** all commands to build, deploy, bootstrap, and test the application are run from within this directory:
* Docker Compose file to deploy Redis database backend, NGINX load balancer, and application
* Simple bootstrap script to load in test data to assist in development

**infra directory:** everything needed to provision a small environment for development and testing:
* Dockerfiles and configuration for Redis and NGINX

**app directory:** the application code:
* Dockerfile and entrypoint script
* *src:* Flask application and requirements file for installing packages via Pip on Docker build
* *src.api:* versions of the API that can be used by the application to fulfill client requests

## Backend
### Creating a distributed Redis cluster

I followed the official guide from Redis Labs here: https://redis.io/topics/cluster-tutorial. They recommend a minimum of 3 master nodes. Each master node has a single replica for a total of 6 cluster nodes.

Additional kernel parameters that should be tuned on the VM:
* ```echo 1 > /proc/sys/vm/overcommit_memory```
* ```echo never > /sys/kernel/mm/transparent_hugepage/enabled```

I chose Redis because of the extremely low-latency requirements of this service. Given its criticality and the potentially large number of URLs served, I spread the data across a sharded cluster that can scale horizontally to meet increased demand. Adding new nodes is a procedure transparent to the application. In order to automate this, we require a service discovery tool to issue the CLUSTER MEET command upon each scale-out event. High availability is guaranteed as each master node in the cluster has a replica that can take over in the event of a master node failure.

## Load balancer
### Distributing work across multiple instances

I configured NGINX to proxy incoming requests and distribute them to multiple instances of the application in a round robin fashion. As the application scales, the NGINX configuration must be updated to include the new server entries. This can be automated using a templating engine and re-deploying the NGINX container with the new configuration.

## Versioning
### Updating the REST endpoint

The version of the API used by the application is loaded dynamically upon start-up, with the version number specified using an environment variable. This allows us to update the API and roll it out incrementally so as to avoid impacting older clients.

## Notes
### Considerations and future work

**Considerations:**
* Multiple Gunicorn worker threads serve the application
* As this service is all in-memory, it can be deployed in Kubernetes or other container orchestration platforms, along with all infrastructure pieces

**Future work:**
* Improve Flask project structure - it's notorious for causing developers to run into issues like circular imports; we can leverage blueprints to improve its structure as complexity increases
* Implement separate data loader - design a service with a queue to upload/update URLs as requests come in; the queue serves as a buffer for incoming requests so that the data loader can scale separately to meet increased demand
