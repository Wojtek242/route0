# Line of three and rogue router topology

```
 ------        ------        ------
|      |      |      |      |      |
|  R1 4|------|4 R2 5|------|4 R3  |
|  5   |      |      |      |      |
 ------        ------        ------
   |
   |
   |
 ------
|  4   |
|  R4  |
|      |
 ------
```

There are three hosts connected to each router, but are not displayed in this
`README`.  For details see their `zebra` and `staticd` configuration files.

## R1

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 127.0.0.1/32
1         | R1-eth1 | 11.0.1.254/24
2         | R1-eth2 | 11.0.2.254/24
3         | R1-eth3 | 11.0.3.254/24
4         | R1-eth4 | 9.0.0.1/24
5         | R1-eth5 | 9.0.4.1/24

## R2

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 127.0.0.1/32
1         | R2-eth1 | 12.0.1.254/24
2         | R2-eth2 | 12.0.2.254/24
3         | R2-eth3 | 12.0.3.254/24
4         | R2-eth4 | 9.0.0.2/24
5         | R2-eth5 | 9.0.1.1/24

## R3

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 127.0.0.1/32
1         | R3-eth1 | 13.0.1.254/24
2         | R3-eth2 | 13.0.2.254/24
3         | R3-eth3 | 13.0.3.254/24
4         | R3-eth4 | 9.0.1.2/24

## R4

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 127.0.0.1/32
1         | R4-eth1 | 13.0.1.254/24
2         | R4-eth2 | 13.0.2.254/24
3         | R4-eth3 | 13.0.3.254/24
4         | R4-eth4 | 9.0.4.2/24
