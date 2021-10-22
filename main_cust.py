# import bankworld_pb2
# import bankworld_pb2_grpc
from Customer import Customer


print ("testing!!!!!!!!!")
cust1 = Customer(1, "withdraw")
print ("testing")
out = cust1.createStub()
print (out)
out2 = cust1.executeEvents()
print (out2)
