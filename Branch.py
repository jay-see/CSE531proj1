from concurrent import futures
import logging
import time
import grpc
import bankworld_pb2
import bankworld_pb2_grpc

class Branch(bankworld_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

        # TODO: students are expected to store the processID of the branches
        pass

    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self, request, context):
        print ("Branch received: " + request.msg)
        self.recvMsg.append(request.msg)
        for i in request.msg:
            if i['interface'] == 'deposit':
                pass
            elif i['interface'] == 'withdraw':
                pass
            elif i['interface'] == 'query':
                time.sleep(3)
                branchmsg = branchmsg + "'money':" + self.balance
        return bankworld_pb2.BranchReply(branch_msg=branchmsg)


