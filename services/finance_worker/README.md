# Run the service

setup .env variables in .env file

before running after changes compile requirements:
```bash
make compile
```

run docker compose 
```bash
docker compose up finance_worker
```


get rabbitmq message:
```bash
make get_message
```