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


def Serve(id, balance, branches):
    channelnumber = 50050+id
#    print ("Starting server. Listening on port " + str(channelnumber), file = of)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bankworld_pb2_grpc.add_BranchServicer_to_server(Branch(id, balance, branches), server)
#    channelnumber = 50050+id
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
#            print (out2, file = of)
            with open("output.json", "a") as thefile:
                thefile.write(out2+"\n")


# Opening JSON file
f = open('input.json',)
data = json.load(f)

def run():
    print ("MAIN THREAD!!!!!!")
# returns JSON object as
# a dictionary
#    data = json.load(f)
    count = 0
    for x in data:
        if x['type'] == 'bank':
            count += 1
#            print ("Starting server. Listening on port " + str(50050+x['id']), file = of)
    for y in data:
        if y['type'] == 'bank':
            print ("Number of banks is " + str(count))
            Serve(y['id'], y['balance'], count)

# Iterating through the json
# list
# print (data[0])


#	       break
run()

if __name__ == '__main__':

    mp.set_start_method('spawn')
#    q = mp.Queue()
#    run()
    for z in data:
        if z['type'] == 'client':
            with open("output.json", "a") as myfile1:
                myfile1.write("Starting server. Listening on port " + str(50050+z['id'])+"\n")

    for i in data:
        if i['type'] == 'client':
            print (i['events'])
            p = mp.Process(target=Cust, args=(i['id'],str(i['events']),))
#            time.sleep(.5)

#            print ("Starting server. Listening on port " + str(50050+i['id']), file = of)
            p.start()
            p.join()
# Closing file
f.close()
