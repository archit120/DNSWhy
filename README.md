# DNSWhy


This repository contains work in progress code for a python DNS query tool. There are no reasons for its existence apart from understanding DNS protocol.

Directory Structure -
 - `manual` - contains scripts I used early on in this project to manually send and interpret DNS messages.
 - `main.py` - logic for resolving domain name
 - `enums.py` - contains subset of enums defined in DNS
 - `network.py` - simple UDP code to send and receive message
 - `packing.py` - convert python structures to bytes for network
 - `unpacking.py` - convert bytes received from network back to python
 - `structures.py` - defines a subset of structures in DNS

## Logic

The recurisve logic is mostly summarized by the below diagram.
![](logic.png)