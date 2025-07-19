# UNetLab

UNetLab is a next-generation software platform for networking labs. It is a complete rewrite of iou-web, designed to provide multi-hypervisor support within a single unified environment. Unlike GNS3 and iou-web, UNetLab allows you to design labs using IOU, Dynamips, and QEMU nodes without managing multiple virtual machines — everything runs inside a single UNetLab host. Labs are saved as a single file containing all the necessary information.

## Prerequisites

* Install Proxmox VE.
* Create a Proxmox API token **without** the `Privilege Separation` flag.

## Running the Server

Install the production dependencies:

```bash
poetry install --without dev
poetry run ./manage.py migrate
poetry run ./manage.py createsuperuser
```

Start the Django development server:

```bash
poetry run ./manage.py runserver
```

## Running Celery Workers and Scheduler

Start the Celery worker:

```bash
poetry run celery -A unetlab worker -l info
```

Start the Celery beat scheduler:

```bash
poetry run celery -A unetlab beat -l info
```

## Development

### Setup Development Environment

To set up the development environment, including dev dependencies, run:

```bash
poetry install --with dev
```

### Run Checks and Tests

To run all pre-commit checks and tests with coverage reporting:

```bash
poetry run pre-commit run --all-files
poetry run coverage run --omit="unetlab/tests/*" -m pytest unetlab
poetry run coverage report -m
poetry run pytest -v
poetry run ./manage.py makemigrations ui job proxmox
```

### Adding New Libraries

To add new packages as development dependencies (for example, pytest and coverage):

```bash
poetry add --dev pytest pytest-django coverage
```
