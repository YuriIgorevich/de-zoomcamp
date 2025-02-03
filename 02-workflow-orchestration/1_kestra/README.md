# Module 2: Workflow Orchestration
## Prerequisites
The setup was created and tested using:
 - Ubuntu 24.04.1 LTS in WSL
 - Docker 27.5.0

## Walk-Through
Kestra and PostgreSQL are deployed via [docker compose](./docker-compose.yml). In postgres 2 databases are created: 
 - `ny_taxi` - created as default DB via setting `POSTGRES_DB` environment variable 
 - `kestra` - created via init [script](./docker/pg-init.sh)