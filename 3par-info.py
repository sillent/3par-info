#!/usr/bin/env python

import sys


try:
    import paramiko
except Exception:
    print "Error. Can't import module 'paramiko'. Exiting."


class Host(object):

    def __init__(self, hostname, username, password, **kwarg):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = 22
        # check kwarg not empty and initialize a other value
        if (kwarg):
            if 'port' in kwarg:
                self.port = int(kwarg['port'])

        self.sshclient = paramiko.SSHClient()

    def connect(self):
        """Method that connect to host machine"""
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.sshclient.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                port=self.port)
            return self
        except paramiko.SSHException as sshe:
            print "Can't connect to host"
            print sshe
            self.sshclient.close()
            sys.exit(1)

    def command_execute(self, command):
        commands[command](self.client)
        # execute need command
        # like check_pd(),
        # check_node(), etc..

    def close_connect(self):
        self.sshclient.close()


def main():
    if len(sys.argv) < 5:
        print "Usage:\n %s \
<hostname > <username > <password> <command>" % sys.argv[0]
        exit(1)


def check_pd(client):
    try:
        stdin, stdout, stderr = client.exec_command("check_pd")
        data
    except client.SSHException:
        print "Command %s fail" % "check_pd"


commands = {"check_pd": check_pd,
            "check_node": check_node,
            "check_ps": check_ps}


if __name__ == '__main__':
    # passw = raw_input("Vvedite parol: ")
    main()
    host = Host(sys.argv[1], sys.argv[2], sys.argv[3])
    host.connect()
    host.command_execute(sys.argv[4])
    host.close_connect()
