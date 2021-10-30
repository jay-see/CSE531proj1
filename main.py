from concurrent import futures
import logging
import grpc
import bankworld_pb2
import bankworld_pb2_grpc
import json
from Customer import Customer
from Branch import Branch
import multiprocessing
import time
import threading

serverlist = list()
finalmsg = list()
bankbranch = list()

def Serve(id, balance, branches):
    channelnumber = 50050+id
#    serverlist = list()
    
    serverlist.append(grpc.server(futures.ThreadPoolExecutor(max_workers=10,)))
    bankbranch.append(Branch(id, balance, branches))
    print ("ID = "+ str(id))
    bankworld_pb2_grpc.add_BranchServicer_to_server(bankbranch[id-1], serverlist[id-1])

    serverlist[id-1].add_insecure_port('[::]:'+str(channelnumber))
#    p = mp.Process(target=server.start(), args=())
    serverlist[id-1].start()
#    try:
#        while True:
#            time.sleep(20)
#    except KeyboardInterrupt:
#        server.stop(None)
#    server.stop(None)
#    p.start()
#    p.join()
    print ("Started SERVER at port "+str(channelnumber))

    out = bankbranch[id-1].createStubsss(branches)
    print ("Created BRANCH SELFSTUB #" + str(id))
    print ("BRANCH create stubsss output: " + out)
    
def Cust(custid, custevents):
#    for i in data:
#        if i['type'] == 'client':
            print (custevents)
            cust = Customer(custid, custevents)
            print ("testing")
            out = cust.createStub()
            print ("create stub output: " + out)
#            return cust
        
#def Custexecute(customer)
            finalmsg.append(cust.executeEvents())
#            with open("output.json", "a") as thefile:
#                thefile.write(out2+"\n")
#                for i in range(len(serverlist)):
#                    thefile.write(
#            return "success"

# Opening JSON file
f = open('input.json',)
data = json.load(f)

def run():
    print ("MAIN THREAD!!!!!!")
# returns JSON object as
# a dictionary
#    data = json.load(f)
    count = 0
    serverlist = list()
#    p2list = list()
    
    for x in data:
        if x['type'] == 'bank':
            count += 1
#            print ("Starting server. Listening on port " + str(50050+x['id']), file = of)
    for y in data:
        if y['type'] == 'bank':
            print ("Number of banks is " + str(count))
            serverlist.append(Serve(y['id'], y['balance'], count))
#            p2 = threading.Thread(target=Serve, args=(y['id'], y['balance'], count,))
#            p2list.append(p2)
#            p2.start()
 #   for p2 in p2list:
 #       p2.join()

#    for z in range(len(serverlist)):
#        out = serverlist[z].createStubsss(count)
#        print ("Created BRANCH SELFSTUB #" + str(z))
#    print ("BRANCH create stubsss output: " + out)
# Iterating through the json
# list
# print (data[0])


#	       break
#run()

if __name__ == '__main__':
    logging.basicConfig()
#    processlist = list()
#    multiprocessing.set_start_method('spawn')
#    q = multiprocessing.Queue()
#    run()
    for z in data:
        if z['type'] == 'client':
            with open("output.json", "a") as myfile1:
                myfile1.write("Starting server. Listening on port " + str(50050+z['id'])+"\n")
    run()
    for i in data:
        if i['type'] == 'client':
            print (i['events'])
            Cust(i['id'],str(i['events']),)

    with open("output.json", "a") as thefile:
        for i in range(len(finalmsg)):
            thefile.write(finalmsg[i])
            # write the final balances to file
            thefile.write(str(bankbranch[i].balance)+"}]}\n")




#            p = multiprocessing.Process(target=Cust, args=(i['id'],str(i['events']),)) 
#            p.start()
#            processlist.append(p)
#    for p in processlist:
#        p.join()

#    for i in range(len(custlist)):
#        out2 = custlist[i].executeEvents()
        
#        with open("output.json", "a") as thefile:
#            thefile.write(out2+"\n")

#            p.start()
#            p.join()
# Closing file
f.close()
