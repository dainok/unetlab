#!/usr/bin/env python

import os
import django
import yaml


data = """
groups:
- template: local-vyos-vyos
  prefix: R
  count: 4
  topology: full-mesh
  link_type: l1
  features:
  - loopback:name=Loopback0
- template: local-vyos-vyos
  prefix: R
  count: 4
  topology: full-mesh
  link_type: l1
  features:
  - loopback:name=Loopback0
- template: local-vyos-vyos
  prefix: R
  count: 8
  topology: hub-spoke
  hubs: 3
  connect_hubs: true
  link_type: l1
  features:
  - loopback:name=Loopback0
- template: local-vyos-vyos
  prefix: R
  count: 6
  topology: ring
  link_type: l1
  features:
  - loopback:name=Loopback0
- template: local-vyos-vyos
  prefix: R
  count: 4
  topology: linear
  link_type: l1
  features:
  - loopback:name=Loopback0
- template: local-vyos-vyos
  prefix: R
  topology: custom
  link_type: l1
  links:
  - R30, R31, R32, R33
  - R30, R31
  - R32, R33
  - R32, R11
  - R33, R10
- template: local-vyos-vyos
  prefix: R
  topology: custom
  link_type: l2
  links:
  - R1, R12
  - R2, R13
  - R5, R14
  - R6, R15
  - R23, R16
  - R20, R17
  - R26, R18
  - R29, R19
  features:
  - loopback:name=Loopback0
interfaces:
- match: Loopback0
  address: 192.168.0.1/16
  mask: 32
  features:
  - ospf:area=0
- match: Ethernet
  address: 10.0.0.0/8
  mask: auto
  features:
  - ospf:area=0
"""


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unetlab.settings")
django.setup()

from lab.models import LabLld, Lab

lab_id=1
lab_obj = Lab.objects.get(pk=lab_id)
lab_obj.hld = yaml.safe_load(data)
lld_obj = LabLld(lab_obj.hld)
lab_obj.lld = lld_obj.to_dict()
lab_obj.save()


#hld_src = yaml.safe_load(hld_data)
#lld = LabLld(hld_src)

#out_lld = lld.to_dict()

from pprint import pprint
#pprint(lab_obj.lld)
