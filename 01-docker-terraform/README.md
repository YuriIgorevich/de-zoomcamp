# Module 1: Docker, SQL and Terraform
## Prerequisites
The setup was created and tested using:
- Ubuntu 24.04.1 LTS in WSL
- Docker 27.5.0 
- Terraform 1.10.4
- pgcli 4.1.0

## Walk-Through
No cloud providers are used, to explore terraform `postgresql` provider can be used. In this scenario `ny_taxi` database is not created (only `postgres` database available) via docker compose but must be created by terraform.

Commands are executed from the project root directory.

### 1. Set up directories 
```bash
export TERRAFORM_DIR="./01-docker-terraform/1_terraform"
export DOCKER_DIR="./01-docker-terraform/2_docker_sql"
```


### 2. Create PostgreSQL database
#### Option 1. Create DB directly
Environment variable `PGDATABASE` must contain desired database name `ny_taxi`.

```bash
export PGDATABASE="ny_taxi"
docker compose --file "${DOCKER_DIR}/docker-compose.yml" up -d
```

#### Option 2. Create DB via terraform
Environment variable `PGDATABASE` must not contain value. Unset variable to ensure that.

```bash
unset PGDATABASE
docker compose --file "${DOCKER_DIR}/docker-compose.yml" up -d
```

Initilaize terraform.
```bash
terraform -chdir="${TERRAFORM_DIR}" init
```

Run terraform plan.
```bash
terraform -chdir="${TERRAFORM_DIR}" plan
```

Run terraform apply.
```bash
terraform -chdir="${TERRAFORM_DIR}" apply
```

### 3. Verify `ny_taxi` database is created

```bash
pgcli -U root -h localhost -p 5432 -d postgres -l
```

### 4. Containerize ingestion script

```bash
docker build \
    -t ny_taxi_ingest:v0.0.1 \
    -f ${DOCKER_DIR}/Dockerfile \
    ${DOCKER_DIR}
```

### 5. Run ingestion script

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
NETWORK_NAME="$(basename $DOCKER_DIR)_default"

docker run -it \
  --network=${NETWORK_NAME} \
  ny_taxi_ingest:v0.0.1 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips \
    --url=${URL}
```

### 6. Shutdown docker compose services

```bash
docker compose --file "${DOCKER_DIR}/docker-compose.yml" down
```