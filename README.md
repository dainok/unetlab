UNetLab is a new generation software for networking lab. It can be considered the next major version of iou-web, but the software has been rewritten from scratch. The major advantage over GNS3 and iou-web itself is about multi-hypervisor support within a single entity. UNetLab allows to design labs using IOU, Dynamips and QEMU nodes without dealing with multi virtual machines: everything run inside a UNetLab host, and a lab is a single file including all information needed.

Install Proxmox VE, and create a token without `Privilege Separation` flag.

Run server:

```bash
./manage.py runserver
```

Run worker:

```bash
celery -A unetlab worker -l info
```

Run scheduler:

```bash
celery -A unetlab beat -l info
```
