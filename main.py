from concurrent import futures
import logging
import grpc
import bankworld_pb2
import bankworld_pb2_grpc
import json
from Customer import Customer
from Branch import Branch
import multiprocessing as mp
import time
#import sys


#from multiprocessing import Process
#import subprocess
#import os
#os.system("unset http_proxy")
#os.system("unset https_proxy")


#subprocess.call(['python3', 'Branch.py'])

def Serve(id, balance, branches):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bankworld_pb2_grpc.add_BranchServicer_to_server(Branch(id, balance, branches), server)
    channelnumber = 50050+id
    server.add_insecure_port('[::]:'+str(channelnumber))
    server.start()

def Cust(custid, custevents):
#    for i in data:
#        if i['type'] == 'client':
            print (custevents)
            cust = Customer(custid, custevents)
            print ("testing")
            out = cust.createStub()
            print ("create stub output: " + out)
            out2 = cust.executeEvents()
            print (out2, file = of)
            

of = open('output.json', 'a')   

Serve(1, 400, 3)
Serve(2, 0, 7)

#subprocess.call(['python3', 'main_cust.py'])

# Opening JSON file
f = open('input.json',)
 
# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
# print (data[0])


#	       break

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()

    for i in data:
        if i['type'] == 'client':
            print (i['events'])
            p = mp.Process(target=Cust, args=(i['id'],str(i['events']),))
            time.sleep(.1)
            p.start()
#            p.join()
# Closing file
f.close()
