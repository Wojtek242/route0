# Four area topology

Topology taken from [this
image](https://networklessons.com/wp-content/uploads/2017/05/xis-is-multiple-areas-adjacencies.png.pagespeed.a.ic.tmdDcRdRK8.png)

```
 ------        ------        ------
|      |      |      |      |      |
|  R5 1|------|3 R6 1|------|2 R9 1|--- h9_1
|  2   |      |  2   |      |      |
 ------        ------        ------
   |             |
   |             |
   |             |
 ------        ------
|  1   |      |  1   |
|  R7 2|------|3 R8  |
|      |      |  2   |
 ------        ------
                 |
                 |
                 |
 ------        ------        ------        ------
|      |      |  1   |      |      |      |      |
|  R1 1|------|3 R2 2|------|3 R3 1|------|1 R4  |
|      |      |      |      |  2   |      |      |
 ------        ------        ------        ------
                               |
                               |
                               |
                              h3_1
```

## R1

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.1/32
1         | R1-eth1 | 10.0.1.1/24

## R2

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.2/32
1         | R2-eth1 | 10.0.2.1/24
2         | R2-eth2 | 10.0.3.1/24
3         | R2-eth3 | 10.0.1.2/24

## R3

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.3/32
1         | R3-eth1 | 10.0.4.1/24
2         | R3-eth2 | 10.3.0.254/24
3         | R3-eth3 | 10.0.3.2/24

## R4

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.4/32
1         | R4-eth1 | 10.0.4.2/24

## R5

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.5/32
1         | R5-eth1 | 10.0.5.1/24
2         | R5-eth2 | 10.0.6.1/24

## R6

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.6/32
1         | R6-eth1 | 10.0.6.1/24
2         | R6-eth2 | 10.0.7.1/24
3         | R6-eth3 | 10.0.5.2/24

## R7

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.7/32
1         | R7-eth1 | 10.0.6.2/24
2         | R7-eth2 | 10.0.8.1/24

## R8

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.8/32
1         | R8-eth1 | 10.0.7.2/24
2         | R8-eth2 | 10.0.2.2/24
3         | R8-eth3 | 10.0.8.2/24

## R9

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.9/32
1         | R9-eth1 | 10.9.0.254/24
2         | R9-eth2 | 10.0.6.2/24

## h3_1

Interface | Name      | Address/Subnet
----------|-----------|---------------
1         | h3_1-eth1 | 10.3.0.1/24

## h9_1

Interface | Name      | Address/Subnet
----------|-----------|---------------
1         | h9_1-eth1 | 10.9.0.1/24

