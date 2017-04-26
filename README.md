#  HP 3PAR monitoring util

This util can monitor HP 3PAR chassis throw SSH.
Util use Python module [`paramiko`](https://github.com/paramiko/paramiko), that means you need install that module before using this script.

The writing of this program was inspired 
## Usage
Script must be running like this:
`./3par-info.py <hostname> <username> <password> <command>`
Where:
`hostname` - IP or domain name of 3PAR CLI management interface
`username` - user name
`password` - password
`command` - guess?       Yes, command that need to be executed
## Supporting command for monitoring
* check_pd
That command execute 'showpd' for getting information about Physical disk
* check_node
That command execute 'shownode' for getting information about Node status
* check_ps
That command execute 'shownode' with argument '-ps' for getting information about Power Supply
* check_vv
That command execute 'showvv' for getting information about Virtual Volume
* check_ld
That command execute 'showld' for getting information about Logical Disk

## Not implemented command
- [] check_port_fc
- [] check_cap_fc
- [] check_cap_nl
