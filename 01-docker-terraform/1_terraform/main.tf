terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "1.25.0"
    }
  }
}

resource "postgresql_database" "db_ny_taxi" {
  name  = var.db_ny_taxi_name
  owner = "root"
}
