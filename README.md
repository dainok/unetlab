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

### Internationalization

```bash
poetry run ./manage.py makemessages -l en
poetry run ./manage.py compilemessages
```

### Run Checks and Tests

To run all pre-commit checks and tests with coverage reporting:

```bash
poetry run pre-commit run --all-files
poetry run coverage run --omit="unetlab/tests/*" -m pytest unetlab
poetry run coverage report -m
poetry run pytest -v
poetry run ./manage.py makemigrations ui job proxmox lab node
```

### Adding New Libraries

To add new packages as development dependencies (for example, pytest and coverage):

```bash
poetry add --dev pytest pytest-django coverage
```

## Testing API using a token

```bash
curl -X POST -H "Authorization: Token d94fef88dbd7c4f70cdec97e880ea7b92286bde0" http://localhost:8000/api
```

## Data Exchange via API

The APIs are built using Django REST Framework, with the output format customized to always include certain fields. The response format is as follows:

```json
{
    "status": "success", // Either "success" or "error"
    "http": {
        "code": 200, // HTTP status code
        "message": "OK", // HTTP status message
        "url": "/api/log", // The requested URL
    },
    "type": "response", // For API requests, this is always "response"
    "data": [], // The server response data, if present
    "traceback": "", // Present only in case of errors (with debug enabled)
}
```

## Data Exchange via WebSocket

The same API response model is adapted for WebSocket communication. Server -> Client messages follow this format:

```json
{
    "type": "event", // For server-to-client events, this is always "event"
    "command": "log-add", // The reverse view name as used by the API
    "data": {}, // The data payload to be sent to the client, if present
}
```

In this case, the client does not need to acknowledge the server's request but simply handle the event.

Client -> Server messages follow this format:

```json
{
    "type": "request", // For client-to-server requests, this is always "request"
    "command": "host-rescan", // The reverse view name as used by the API
    "data": {}, // The data payload to send to the server
}
```

Server responses to client requests follow this format:

```json
{
    "status": "success", // Either "success", "error", or "queued"
    "type": "response", // For responses to client requests, this is always "response"
    "command": "host-rescan", // The command requested by the client
    "data": {}, // The response payload to send back to the client
    "traceback": "", // Present only in case of errors (with debug enabled)
}
```
