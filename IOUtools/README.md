# IOU Tools

## Overview

IOU tools are used to manipulate the IOU NVRAM file.

The following tools are available:

- iou_export: exports startup/private configuration from IOU NVRAM file.
- iou_import: imports startup/private configuration into IOU NVRAM file.

The IOU tools are based on Dynamips, see https://github.com/GNS3/dynamips

## License

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

The full license text is available in the file LICENSE.

## Requirements

Python 2.7 or 3.x is needed. Only standard modules are used.

## Limitations

- When iou_import creates a new NVRAM image, it can't know, which IOU
  it will use. Therefore on the first saving of the startup-config
  within IOU you might get the warning
  "Attempting to overwrite an NVRAM configuration previously written
   by a different version of the system image."

  You can ignore this warning.

  This doesn't happen, if an existing NVRAM image is updated by iou_import.

- iou_import will not compress the startup-configuration.

  Therefore if you extract a compressed configuration with iou_export
  and then re-import it with iou_import, the NVRAM usage will increase.
  If the flash size is quite small, you might get the error message
  "NVRAM size too small".

  In this case increase the NVRAM size.

