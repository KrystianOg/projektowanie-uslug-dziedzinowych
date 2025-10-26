# projektowanie-uslug-dziedzinnowych

## Directory Structure

```bash
.
├── infrastructure/
│   ├── docker-compose.yaml # Main service definitions
│   ├── .env.example        # Example environment configuration
│   └── Makefile            # Helper scripts for setup 
├── dashboard/
├── services/
│   ├── api_gateway/
│   ├── finance_worker/
│   ├── ml_processor/
│   ├── social_worker/
│   └── trade_executor/
└── tests/
    ├── e2e/
    └── integration/
```

## Local Environment Setup

> [!NOTE]
> all below commands are executed from the `infrastructure/` directory.

### 1. Configure Environment Variables

Start by copying the example environment file:

```bash
cp .env.example .env
```

This creates a local `.env` file containing initial development variables.
Review the file and fill in any missing values - some services may fail to start without them.

**Required API Keys**

To use the Alpaca Trading API, create an account at [Alpaca](https://alpaca.markets/) and obtain your credentials.
- **Paper Account:** in the top-left corner of the dashboard, select or create a **Paper** account. This mode is for development and testing strategies - it does **not** involve real money.
- **API Keys:** Available under [Profile Settings &rarr; Manage Accounts](https://app.alpaca.markets/user/profile#manage-accounts)
  Each user can create up to **three** paper accounts.

> [!CAUTION]
> Never share or commit your API keys.

---
### 2. Build and Run Containers

Once all secrets are configured, build and start the local environment:

```bash
docker compose up --build
```

This will pull required images (if not cached) and start all services defined in the Docker Compose configuration.

> [!TIP]
> For more docker compose commands refer to [infrastructure/Makefile](infrastructure/Makefile) or [Docker Compose documentation](https://docs.docker.com/compose/)

## Local Services Development

Python services in this project use `uv` as the package manager.
For installation insttructions, see the official [uv documentation](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

To compile the dependencies for all services at once, run the following command from the **root project directory**.

```bash
make compile-all
```

This will generate or update `requirements.txt` for every service that contains a `uv.lock` file, ensuring all dependencies are in sync across the project.