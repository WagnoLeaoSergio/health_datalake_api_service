# health_datalake_api_service

API para gerenciamento dos dados de sinais vitais usados no sistema implementado no TCC.

## Installation

From source:

```bash
git clone https://github.com/WagnoLeaoSergio/health_datalake_api_service health_datalake_api_service
cd health_datalake_api_service
make install
```

From pypi:

```bash
pip install health_datalake_api_service
```

## Executing

This application has a CLI interface that extends the Flask CLI.

Just run:

```bash
$ health_datalake_api_service
```

or

```bash
$ python -m health_datalake_api_service
```

To see the help message and usage instructions.

## First run

```bash
health_datalake_api_service create-db   # run once
health_datalake_api_service populate-db  # run once (optional)
health_datalake_api_service add-user -u admin -p 1234  # ads a user
health_datalake_api_service run
```

Go to:

- Website: http://localhost:5000
- Admin: http://localhost:5000/admin/
  - user: admin, senha: 1234
- API GET:
  - http://localhost:5000/api/v1/**


> **Note**: You can also use `flask run` to run the application.
