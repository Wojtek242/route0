# Four area topology

Topology taken from [this
image](https://networklessons.com/wp-content/uploads/2017/05/xis-is-multiple-areas-adjacencies.png.pagespeed.a.ic.tmdDcRdRK8.png)

```
 ------A3      ------A3      ------A4
|      |      |      |      |      |
|  R5 1|------|3 R6 1|------|2 R9 1|--- h9_1
|  2   |      |  2   |      |      |
 ------        ------        ------
   |             |
   |             |
   |             |
 ------A3      ------A3
|  1   |      |  1   |
|  R7 2|------|3 R8  |
|      |      |  2   |
 ------        ------
                 |
                 |
                 |
 ------A1      ------A1      ------A2      ------A2
|      |      |  1   |      |      |      |      |
|  R1 1|------|3 R2 2|------|3 R3 1|------|1 R4  |
|      |      |      |      |  2   |      |      |
 ------        ------        ------        ------
                               |
                               |
                               |
                              h3_1
```

## Area 1

Area ID: 49.0001

### R1

* NET: 49.0001.0100.0000.0001.00
* IS-type: level-1

Interface | Name    | Circuit Type
----------|---------|---------------
0         | lo      | -
1         | R1-eth1 | Level-1

### R2

* NET: 49.0001.0100.0000.0002.00
* IS-type: level-1-2

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R2-eth1 | Level-2
2         | R2-eth2 | Level-2
3         | R2-eth3 | Level-1

## Area 2

Area ID: 49.0002

### R3

* NET: 49.0002.0100.0000.0003.00
* IS-type: level-1-2

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R3-eth1 | Level-1
2         | R3-eth2 | -
3         | R3-eth3 | Level-2

### R4

* NET: 49.0002.0100.0000.0004.00
* IS-type: level-1

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R4-eth1 | Level-1

## Area 3

Area ID: 49.0003

### R5

* NET: 49.0003.0100.0000.0005.00
* IS-type: level-1

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R5-eth1 | Level-1
2         | R5-eth2 | Level-1

### R6

* NET: 49.0003.0100.0000.0006.00
* IS-type: level-1-2

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R6-eth1 | Level-2
2         | R6-eth2 | Level-1-2
3         | R6-eth3 | Level-1

### R7

* NET: 49.0003.0100.0000.0007.00
* IS-type: level-1

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R7-eth1 | Level-1
2         | R7-eth2 | Level-1

### R8

* NET: 49.0003.0100.0000.0008.00
* IS-type: level-1-2

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R8-eth1 | Level-1-2
2         | R8-eth2 | Level-2
3         | R8-eth3 | Level-1

## Area 4

Area ID: 49.0004

### R9

* NET: 49.0004.0100.0000.0009.00
* IS-type: level-2-only

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | -
1         | R9-eth1 | -
2         | R9-eth2 | Level-2
