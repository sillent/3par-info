#!/usr/bin/env python

# Copyright (C) 3par-info: Dmitry Ulyanov <sillent1987@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
try:
    import paramiko
except Exception:
    print("Error. Cant import module paramiko. Exiting")


class Host(object):
    "Host class contains all information needed for connect to",
    "host via module 'paramiko'"

    def __init__(self, hostname, username, password, **kwarg):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = 22
        # check kwarg not empty and initialize a other value
        if (kwarg):
            if 'port' in kwarg:
                try:
                    self.port = int(kwarg['port'])
                except ValueError:
                    print("Wrong parameter port definition")
                    sys.exit(1)
        self.timeout = 2
        self.sshclient = paramiko.SSHClient()

    def connect(self):
        """Method that connect to host machine"""
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.sshclient.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                port=self.port)
            return self
        except paramiko.SSHException as sshe:
            print("Can't connect to host")
            print(sshe)
            self.sshclient.close()
            sys.exit(1)

    def command_execute(self, command):
        """For executing command on host need call this method with available
        command"""
        if command in commands:
            commands[command](self.sshclient)
        else:
            print("Command '%s' not found" % command)

    def close_connect(self):
        """Close connection on host"""
        self.sshclient.close()


# external methods definition
def ssh_command_executor(sshclient, command):
    """Execute SSH command and return buf of data or None if execution command
    failed"""
    try:
        stdin, stdout, stderr = sshclient.exec_command(command)
        buf = stdout.read()
        return buf
    except paramiko.SSHException:
        print("Command '%s' not executing" % command)
        sshclient.close()
        sys.exit(1)


def check_pd_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "State" in line:     # adding header for printing
            ret_data.append(line.split(" "))
        elif "degraded" in line.lower():
            # return data as [id, state, port]
            ret_data.append(line.split(" "))
        elif "failed" in line.lower():
            ret_data.append(line.split(" "))
    return ret_data


def check_node_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Node" in line:      # adding header for printing
            ret_data.append(line.split(" "))
        elif "degraded" in line.lower():
            ret_data.append(line.split(" "))
        elif "failed" in line.lower():
            ret_data.append(line.split(" "))
    return ret_data


def check_ps_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Node" in line:
            ret_data.append(line.split(" "))
        elif "degraded" in line.lower():
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
        elif "failed" in line.lower():
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
        elif "notpresent" in line.lower():
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
    return ret_data


def check_vv_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Name" in line:
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
        elif "degraded" in line.lower():
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
        elif "failed" in line.lower():
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
    return ret_data


def check_ld_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Name" in line:
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
        elif "degraded" in line.lower():
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
        elif "failed" in line.lower():
            str_list = filter(None, line.split(" "))
            ret_data.append(str_list)
    return ret_data

# command definition for exec_command call


def command_check_pd(client):
    try:
        data = ssh_command_executor(client,
                                    "showpd -showcols Id,State")
        status = check_pd_worker(data)
        if len(status) > 1:
            print("CRITICAL! Physical disk degraded or failed. Contact HP Support")
            for i in status:
                print(i)
        else:
            print("NORMAL! All physical disk is OK")
    except paramiko.SSHException:
        print("Command 'check_pd fail")


def command_check_node(client):
    try:
        data = ssh_command_executor(client,
                                    "shownode -showcols Node,State")
        status = check_node_worker(data)
        if len(status) > 1:
            print("CRITICAL! Node failed. Contact HP Support")
            for i in status:
                print(i)
        else:
            print("NORMAL! All node is OK!")
    except paramiko.SSHException:
        print("Command 'check_node' fail")


def command_check_ps(client):
    try:
        data = ssh_command_executor(client,
                                    "shownode -ps -showcols Node,PS,ACState,DCState,PSState")
        status = check_ps_worker(data)
        if len(status) > 1:
            print("CRITICAL! Power suply degraded. Contact HP Support")
            for i in status:
                print(i)
        else:
            print("NORMAL! All power supply works fine")
    except paramiko.SSHException:
        print("Command 'check_ps' fail")


def command_check_ps_cage(client):
    pass


def command_check_vv(client):
    try:
        data = ssh_command_executor(client,
                                    "showvv -showcols Name,State")
        status = check_vv_worker(data)
        if len(status) > 1:
            print("CRITICAL! Virtual volume degraded. Contact HP Support")
            for i in status:
                print(i)
        else:
            print("NORMAL! All virtual volume works fine")
    except paramiko.SSHException:
        print("Command 'check_vv' fail")


def command_check_ld(client):
    try:
        data = ssh_command_executor(client,
                                    "showld -state")
        status = check_ld_worker(data)
        if len(status) > 1:
            print("CRITICAL! Logical Disk degraded. Contact HP Support")
            for i in status:
                print(i)
        else:
            print("NORMAL! All logical disk works fine")
    except paramiko.SSHException:
        print("Command 'check_ld' fail")


# TODO: implement this function


def command_check_port_fc(client):
    pass


def command_check_cap_fc(client):
    pass


def command_check_cap_nl(client):
    pass


commands = {"check_pd": command_check_pd,
            "check_node": command_check_node,
            "check_ps": command_check_ps,
            "check_ps_cage": command_check_ps_cage,
            "check_vv": command_check_vv,
            "check_ld": command_check_ld,
            "check_port_fc": command_check_port_fc,
            "check_cap_fc": command_check_cap_fc,
            "check_cap_nl": command_check_cap_nl}


def main():
    if len(sys.argv) < 5:
        print("Usage:\n %s \
<hostname > <username > <password> <command>" % sys.argv[0])
        print("command: ")
        for command in commands:
            print("\t%s" % command)
        exit(1)


if __name__ == '__main__':
    main()
    script, hostname, username, password, command = sys.argv
    # host = Host(sys.argv[1], sys.argv[2], sys.argv[3])
    host = Host(hostname, username, password)
    host.connect()
    host.command_execute(command)
    host.close_connect()
    sys.exit(0)
