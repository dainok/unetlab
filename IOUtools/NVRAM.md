# NVRAM Structure

This documents the IOU NVRAM structure. It is based on the information
in dynamips' fs_nvram.h, see
https://github.com/GNS3/dynamips/blob/master/common/fs_nvram.h

Only the first half of the NVRAM is used, the second half is zero filled.

The structure is almost identical to the Dynamips NVRAM layout.
The major difference is the missing NVRAM header in IOU.

| Layout of first half  |
|-----------------------|
| Startup Header        |
| Startup Configuration |
| Padding               |
| Private Header        |
| Private Configuration |
| Free Space            |
| File Area             |

All data is stored in big endian order, high byte first.


## Startup Header

| Off | Len | Usage                           |
|----:|----:|---------------------------------|
|   0 |   2 | Magic 0xABCD                    |
|   2 |   2 | Format, 1 = raw, 2 = compressed |
|   4 |   2 | Checksum                        |
|   6 |   2 | IOS version, 0x0F04 = 15.4      |
|   8 |   4 | Start address                   |
|  12 |   4 | End address                     |
|  16 |   4 | Length                          |
|  20 |   4 | ??? 0                           |
|  24 |   4 | ??? 0 = raw, 1 = compressed     |
|  28 |   2 | ??? 0 = raw, 1 = compressed     |
|  30 |   2 | ??? 0                           |
|  32 |   4 | uncompressed len, raw = 0       |

Total 36 bytes

The checksum is basically the sum of all 2-byte-words in the first half
of the NVRAM. For further details have a look into iou_import, function
checksum.


## Startup Configuration

In raw format the configuration is stored without any changes.
In compressed format, the configuration is compressed the same
way as in the unix compress program, see
http://en.wikipedia.org/wiki/Compress .
It uses the LZW algorithm.


## Padding

The startup-config is padded to an aligment of 4.
In IOS <= 15.0, if padding takes places, an additional 4 byte
padding is added.


## Private Header

| Off | Len | Usage                           |
|----:|----:|---------------------------------|
|   0 |   2 | Magic 0xFEDC                    |
|   2 |   2 | Format, only 1 = raw            |
|   4 |   4 | Start address                   |
|   8 |   4 | End address                     |
|  12 |   4 | Length                          |

Total 16 bytes


## Private Configuration

The private configuration is always stored in raw format.


## File Area

The files are growing top-down. Each file block is 1024 bytes long and
starts with the magic number 0xDCBA. An unused/erased block is all zero.
