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
from __future__ import print_function
import sys
import re
import pickle
try:
    import paramiko
except Exception:
    print("Error. Cant import module paramiko. Exiting")


ARG_COUNT = 5
degrad = "degraded"
fail = "failed"
npres = "notpresent"

# messages:
critical = "CRITICAL! "
normal = "NORMAL! "
disk_fail_message = "Physical disk degraded or failed. Contact HP Support"
disk_ok_message = "All physical disk is OK"
node_fail_message = "Node degraded or failed. Contact HP Support"
node_ok_message = "All node is OK"
ps_fail_message = "Power supply failed or degraded. Contact HP Support"
ps_ok_message = "All power supply is OK"
vv_fail_message = "Virtual volume failed or degraded. Contact HP Support"
vv_ok_message = "All virtual volume is OK"
ld_fail_message = "Logical Disk failed or degraded. Contact HP Support"
ld_ok_message = "All logical disk is OK"


class Host(object):
    "Host class contains all information needed for connect to",
    "host via module 'paramiko'"

    def __init__(self, hostname, username, password, **kwarg):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = kwarg.get("port", 22)
        self.timeout = kwarg.get("timeout", 2)
        # initialize paramiko SSHClient
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
        elif degrad in line.lower():
            ret_data.append(line.split(" "))
        elif fail in line.lower():
            ret_data.append(line.split(" "))
    return ret_data


def check_node_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Node" in line:      # adding header for printing
            ret_data.append(line.split(" "))
        elif degrad in line.lower():
            ret_data.append(line.split(" "))
        elif fail in line.lower():
            ret_data.append(line.split(" "))
    return ret_data


def filter_fun(line):
    return filter(None, line.split(" "))


def check_ps_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Node" in line:
            ret_data.append(line.split(" "))
        elif degrad in line.lower():
            str_list = filter_fun(line)
            ret_data.append(str_list)
        elif fail in line.lower():
            str_list = filter_fun(line)
            ret_data.append(str_list)
        elif npres in line.lower():
            str_list = filter_fun(line)
            ret_data.append(str_list)
    return ret_data


def check_vv_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Name" in line:
            str_list = filter_fun(line)
            ret_data.append(str_list)
        elif degrad in line.lower():
            str_list = filter_fun(line)
            ret_data.append(str_list)
        elif fail in line.lower():
            str_list = filter_fun(line)
            ret_data.append(str_list)
    return ret_data


def check_ld_worker(data):
    ret_data = []
    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if "Name" in line:
            str_list = filter_fun(line)
            ret_data.append(str_list)
        elif degrad in line.lower():
            str_list = filter_fun(line)
            ret_data.append(str_list)
        elif fail in line.lower():
            str_list = filter_fun(line)
            ret_data.append(str_list)
    return ret_data


def stat_cpu_worker(data):
    node_usr = {}
    node_sys = {}
    node_idl = {}
    node_intr = {}
    node_ctxt = {}
    ret_data = []
    reg = re.compile("\d,total")

    for line in (data.decode("utf-8")).split('\n'):
        line = line.strip()
        if reg.match(line):
            line_sep = filter_fun(line)
            if sys.version_info[0] == 2:
                node_usr[int(line[0])] = int(line_sep[1])
                node_sys[int(line[0])] = int(line_sep[2])
                node_idl[int(line[0])] = int(line_sep[3])
                node_intr[int(line[0])] = int(line_sep[4])
                node_ctxt[int(line[0])] = int(line_sep[5])
            elif sys.version_info[0] == 3:
                node_id = next(line_sep)
                node_usr[int(line[0])] = next(line_sep)
                node_sys[int(line[0])] = next(line_sep)
                node_idl[int(line[0])] = next(line_sep)
                node_intr[int(line[0])] = next(line_sep)
                node_ctxt[int(line[0])] = next(line_sep)
    ret_data.append({'usr': node_usr})
    ret_data.append({'sys': node_sys})
    ret_data.append({'idl': node_idl})
    ret_data.append({'intr': node_intr})
    ret_data.append({'ctxt': node_ctxt})
    return ret_data
# command definition for exec_command call


def command_check_pd(client):
    try:
        data = ssh_command_executor(client,
                                    "showpd -showcols Id,State")
        status = check_pd_worker(data)
        if len(status) > 1:
            print(critical + disk_fail_message)
            for i in status:
                print(i)
        else:
            print(normal + disk_ok_message)
    except paramiko.SSHException:
        print("Command 'check_pd fail")


def command_check_node(client):
    try:
        data = ssh_command_executor(client,
                                    "shownode -showcols Node,State")
        status = check_node_worker(data)
        if len(status) > 1:
            print(critical + node_fail_message)
            for i in status:
                print(i)
        else:
            print(normal + node_ok_message)
    except paramiko.SSHException:
        print("Command 'check_node' fail")


def command_check_ps(client):
    try:
        data = ssh_command_executor(
            client,
            "shownode -ps -showcols Node,PS,ACState,DCState,PSState")
        status = check_ps_worker(data)
        if len(status) > 1:
            print(critical + ps_fail_message)
            for i in status:
                print(i)
        else:
            print(normal + ps_ok_message)
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
            print(critical + vv_fail_message)
            for i in status:
                print(i)
        else:
            print(normal + vv_ok_message)
    except paramiko.SSHException:
        print("Command 'check_vv' fail")


def command_check_ld(client):
    try:
        data = ssh_command_executor(client,
                                    "showld -state")
        status = check_ld_worker(data)
        if len(status) > 1:
            print(critical + ld_fail_message)
            for i in status:
                print(i)
        else:
            print(normal + ld_ok_message)
    except paramiko.SSHException:
        print("Command 'check_ld' fail")


# TODO: implement this functions


def command_check_port_fc(client):
    pass


def command_check_cap_fc(client):
    pass


def command_check_cap_nl(client):
    pass


def stat_cpu_write_file(data):
    '''xWrite data into file with pickling them before.'''
    _3par_host = sys.argv[1]
    stat_cpu_file_name = "/tmp/%s-cpu.stat" % _3par_host
    try:
        # pickling data into file
        with open(stat_cpu_file_name, "wb") as fi:
            pickle.dump(data, fi, protocol=0)
    except Exception:
        print("Cannot open file %s for writing" % stat_cpu_file_name)


def stat_cpu(client):
    try:
        # show only total cpu usage for node
        data = ssh_command_executor(client,
                                    "statcpu -iter 1 -t")
        status = stat_cpu_worker(data)
        len_of_node = len(status[0]['usr'])
        ret_data_substr = ", "
        arr_of_node_count = []
        # write status data to store values of cpu load
        stat_cpu_write_file(status)

        # return data for discovering zabbix
        for coun in range(len_of_node):
            arr_of_node_count.append('{"{#NODELEN}": "%d"}' % coun)

        ret_str = '{"data":[%s]}' % ret_data_substr.join(arr_of_node_count)
        # python3 print
        print(ret_str, end='')
    except paramiko.SSHException:
        print("Command 'stat_cpu' fail")


commands = {"check_pd": command_check_pd,
            "check_node": command_check_node,
            "check_ps": command_check_ps,
            "check_ps_cage": command_check_ps_cage,
            "check_vv": command_check_vv,
            "check_ld": command_check_ld,
            "check_port_fc": command_check_port_fc,
            "check_cap_fc": command_check_cap_fc,
            "check_cap_nl": command_check_cap_nl,
            "stat_cpu": stat_cpu}


def main():
    if len(sys.argv) < ARG_COUNT:
        print("Usage:\n %s \
<hostname > <username > <password> <command>" % sys.argv[0])
        print("command: ")
        for command in commands:
            print("\t%s" % command)
        sys.exit(1)


if __name__ == '__main__':
    main()
    script, hostname, username, password, command = sys.argv
    host = Host(hostname, username, password)
    host.connect()
    host.command_execute(command)
    host.close_connect()
    sys.exit(0)
