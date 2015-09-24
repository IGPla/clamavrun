# -*- coding: utf-8 -*-
"""
ClamAV antivirus control script
"""
import subprocess
import re
import smtplib
import sys
import socket
import argparse

def install_clamav():
    """
    Install clamav
    """
    cmd = "apt-get install clamav -y"
    subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, executable="/bin/bash").stdout.read()
    
def refresh_clamav():
    """
    Update clamav database
    """
    cmd = "freshclam"
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, executable="/bin/bash").stdout.read()
    
def perform_scan(scan_file, append_file):
    """
    Perform scan with clamav and get results
    """
    cmd = "clamscan -r %s" % scan_file
    executor = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash")
    clamscan_result = executor.stdout.read().split("\n")
    notok = re.compile("FOUND")
    tocheck = [line for line in clamscan_result[0:-10] if line and re.search(notok, line)]
    resultset = []
    resultset.append(u"-- To check --")
    resultset.append(u'\n'.join(tocheck))
    resultset.append(u"-- Summary --")
    resultset.append(u'\n'.join(clamscan_result[-10:]))
    with open(append_file, "a") as fd:
        content = u'\n'.join(resultset)
        fd.write(content.encode("utf-8"))
    return len(tocheck), u'\n'.join(resultset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ClamAV antivirus control script")
    parser.add_argument('-i', '--install', help="Install clamav. Privileged command", action='store_true')
    parser.add_argument('-u', '--update', help="Update ClamAV database", action='store_true')
    parser.add_argument('-s', '--scan', help="Perform scan on the given path", action='store_true')
    parser.add_argument('--scanpath', help="Path where scan will be performed")
    parser.add_argument('--scanoutputfile', help="Scan output filepath", default="/tmp/clamavrun.log")

    userargs = parser.parse_args()

    if not userargs.install and not userargs.update and not userargs.scan:
        print "No one command requested"
        parser.print_help()
        exit(0)

    if userargs.install:
        print "Installing clamav..."
        install_clamav()
        print "Clamav installed"
    if userargs.update:
        print "Updating database..."
        refresh_clamav()
        print "Database updated"
    if userargs.scan:
        print "Start scanning..."
        warnings, scan_result = perform_scan(userargs.scanpath, userargs.scanoutputfile)        
        print u"Scanner log: \n%s\n\nScanner finished. Found %i warnings." % (scan_result, warnings)
