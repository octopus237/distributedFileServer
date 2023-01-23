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

import rpyc, random, os
import pandas as pd
from rpyc.utils.server import ThreadedServer
from rpyc.utils.authenticators import SSLAuthenticator
from rpyc.lib import setup_logger


class MasterServer(rpyc.Service):

    class exposed_Master():
        DN_LIST = [[os.environ["NODE2_IP"], os.environ["NODE2_PORT"], os.environ["NODE2_PATH"]],       # Define the expected number of Datanodes ...
                    [os.environ["NODE1_IP"], os.environ["NODE1_PORT"], os.environ["NODE1_PATH"]]]

        global filemap
        

# Client functions
        @staticmethod
        def exposed_Matchfile(key):                # Matches the keyword and returns only the matching files 
            mf = MasterServer.exposed_Master.exposed_filemap()
            result = mf[mf['Name'].str.contains(key)]
            print (result)
            rdict = result.to_dict('records')
            print (rdict)
            return (rdict)
            

        @staticmethod
        def exposed_select_dn():
            dn = random.choice(__class__.DN_LIST)    # Randomly selects one of the DNodes in DN_LIST
            return (dn)   


        @staticmethod
        def exposed_filemap():                         # Function to get the list of files from all the Dnodes
            filetable = []
            for DN in __class__.DN_LIST:              # Iterating through the DNodes
                dcon = rpyc.connect(DN[0],DN[1])      # connect to DNode (host,port)
                dn = dcon.root.DNode()                # Allows calling of exposed remote DNode server functions
                temptable = filetable
                filemap = dn.filequery()   # Exectutes the 'exposed_filequery()' function in DNode & returns values
                print (type(filemap), "\n", filemap)   # returns a <netref class 'rpyc.core.netref.builtins.list'> object
                filemap= list(filemap)                 # Convert to list object
                filetable = temptable + filemap        # Appends the file list to the existing list 
            print (filetable)               
            df = pd.DataFrame(filetable)               # Converts the list of dictionaries to dataframe 
            print (df.to_string(index=False))
            return (df)


if __name__ == "__main__":
    host = os.environ["DEFAULT_HOST"]
    port = input("Enter the server port [Default = 8080]:")   # Allows user to enter a port number for Server
    if port:
         port = int(port)
    else:
        port = int(os.environ["DEFAULT_PORT"])   

    #authenticator = SSLAuthenticator("private.key", "server.crt")    
                                 # Sets default value as 18812 if no port number is specified by user 
    t = ThreadedServer(MasterServer, hostname=host, port=port, protocol_config={'allow_public_attrs': True})
    """ 'allow_public_attrs' creates the Threaded RPyc server to allow the attributes to be accessible to users 
                                                   i.e. allow normal actions on dict, dataframes """
    setup_logger(quiet=False, logfile=None)     # Start logging online
    t.start()                                   # Start the MasterServer