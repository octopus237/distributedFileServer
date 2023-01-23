#!/usr/bin/python

"""
Project Name: A Secured Distributed File Sharing System

Project Authors: 
[+] Name: Abdullah Al Noman
    [+]Email: a.noman@innopolis.university
[+] Mougoue Kakanou Rolly
    [+] r.mougouekakanou@innopolis.university
[+] Name: Tankoua Njassep Jorest Brice
    [+] Email: j.tankouanjassep@innopolis.university
"""

import abdullahNodeConfig
import os, rpyc, subprocess
from distutils.debug import DEBUG
from datetime import  datetime as dt
from rpyc.utils.server import ThreadedServer
from rpyc.utils.authenticators import SSLAuthenticator
from rpyc.lib import setup_logger

#global IP,PORT,PATH
#IP,PORT,PATH = abdullahNodeConfig.nodeHost,abdullahNodeConfig.nodePort,abdullahNodeConfig.nodePath
timeformat = "%Y-%m-%d %H:%M:%S"                        # Used to print Modified time for files

class AbdullahNode(rpyc.Service):
    class exposed_DNode():

        @staticmethod
        def exposed_filequery():
            print (abdullahNodeConfig.nodePath)
            filelist = []                                       # Create a null file list to append data while iterating
            for (dirpath, dirnames, filename) in os.walk(abdullahNodeConfig.nodePath): # iterating through each folder/ file in PATH
                for file in filename:
                    tempdict = {}                               # Creating a temporary dictionary to record file attributes
                    tempdict['DN_IP'] = abdullahNodeConfig.nodeHost                      # Assigning values for current file to th temp dict
                    tempdict['DN_Port']  = abdullahNodeConfig.nodePort
                    tempdict['Location'] = dirpath
                    tempdict['Name'] = file
                    tempdict['Size'] = os.path.getsize(os.path.join(dirpath,file))          # need to specify full path+filename to get the filesize as only filename is not recognized
                    mtime = dt.fromtimestamp(os.path.getmtime(os.path.join(dirpath,file)))  # This returns a datetime object datetime.datetime(YYYY, MM, DD, hh, mm, ss, ms)
                    tempdict['ModTime'] = mtime.strftime(timeformat)                        # Formats the mtime to "YYYY-MM-DD hh:mm:ss" which is human readable
                    filelist.append(tempdict)                           # Appends each file to the filelist
            print (filelist)
            return (filelist)

if __name__ == "__main__":

    #authenticator = SSLAuthenticator("abdullahNode.key", "abdullahNodeCert.crt")

    t1 = ThreadedServer(AbdullahNode, hostname=abdullahNodeConfig.nodeHost, port=abdullahNodeConfig.nodePort, protocol_config={'allow_public_attrs': True})
                                                # 'allow_public_attrs' is needed to make the rpyc items visible. If this is not specified, it will result in errors
                                                # .. since rpyc dicts & lists are not visible as normal dict and list 
                                                # e.g. while converting an rpyc list of dict (filelist) to dataframe, it returns 'keys' error
    setup_logger(quiet=False, logfile=DEBUG)
    subprocess.Popen("python abdullahFtpServer.py", shell=True) # this opens the ftpserver1.py file in a new console window (shell=True) so that we can view the FTP logs
    t1.start()                                  # Start the DNode server

""" NOTE:
Here we call the ftpserver script separately as including teh FTP script in this file 
creates collision between the rpyc logging and ftp logging & it was difficult to run both simultaneously
USing a new window for FTPserver fixes this issue
"""