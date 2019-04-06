# One node topology

```
         ------ 
        |      |
h1_1 ---|1 R1 2|--- h2_1
        |      |
         ------ 
```

## R1

Interface | Name    | Address/Subnet
----------|---------|---------------
0         | lo      | 10.0.0.1/32
1         | R1-eth1 | 10.1.0.254/24
2         | R1-eth2 | 10.2.0.254/24

## h1_1

Interface | Name      | Address/Subnet
----------|-----------|---------------
1         | h1_1-eth1 | 10.1.0.1/24

## h2_1

Interface | Name      | Address/Subnet
----------|-----------|---------------
1         | h2_1-eth1 | 10.2.0.1/24
