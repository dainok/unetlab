# UNetLab

UNetLab is a next-generation software platform for networking labs. It is a complete rewrite of iou-web, designed to provide multi-hypervisor support within a single unified environment. Unlike GNS3 and iou-web, UNetLab allows you to design labs using IOU, Dynamips, and QEMU nodes without managing multiple virtual machines — everything runs inside a single UNetLab host. Labs are saved as a single file containing all the necessary information.

## Prerequisites

* Install Proxmox VE.
* Create a Proxmox API token **without** the `Privilege Separation` flag.

## Running the Server

Install the production dependencies:

```bash
poetry install --without dev
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

To set up the development environment, including dev dependencies:

```bash
poetry install --with dev
poetry lock
poetry run pre-commit run -a
poetry run pytest --ds=unetlab.settings --cov=. -v
```
