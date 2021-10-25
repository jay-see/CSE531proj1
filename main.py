from concurrent import futures
import logging
import grpc
import bankworld_pb2
import bankworld_pb2_grpc
import json
from Customer import Customer
from Branch import Branch
import subprocess

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
for i in data:
	if i['type'] == 'client':
		print(i['events'])
		cust = Customer(i['id'], i['events'][0]['interface'])
		print ("testing")
		out = cust.createStub()
		print (out)
		out2 = cust.executeEvents()
		print (out2)
#		break

# Closing file
f.close()
