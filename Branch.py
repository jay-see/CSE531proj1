from concurrent import futures
import logging
import time
import grpc
import bankworld_pb2
import bankworld_pb2_grpc
import json

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

    def Query(self):
        return self.balance
    
    def Deposit(self, amount):
        new_bal = self.balance + amount
        if new_bal >= 0:
            self.balance = new_bal
            return "success"
        else:
            return "fail"

    def Withdraw(self, amount):
        new_bal = self.balance - amount
        if new_bal >= 0:
            self.balance = new_bal
            return "success"
        else:
            return "fail"
        
    def MsgDelivery(self, request, context):
        print ("Branch received: " + request.msg)
        branchmsg = "{\'id\': " + str(self.id) + ", \'recv\': [{\'interface\': "
        self.recvMsg.append(request.msg)
        request.msg = request.msg.replace("\'", "\"")
        print ("message after replacement is "+request.msg)
        reqmsg = json.loads(request.msg)
        for i in reqmsg:
            if i['interface'] == 'deposit':
                branchmsg = branchmsg + "\'deposit\', \'result\': "
                result = Branch.Deposit(self,i['money'])
                branchmsg = branchmsg + "\'" + result + "\'}, {\'interface\': "
            elif i['interface'] == 'withdraw':
                branchmsg = branchmsg + "\'withdraw\', \'result\': "
                result = Branch.Withdraw(self,i['money'])
                branchmsg = branchmsg + "\'" + result + "\'}, {\'interface\': "
            elif i['interface'] == 'query':
                time.sleep(3)
                bal = Branch.Query(self)
                branchmsg = branchmsg + "\'query\', \'result\': 'success', \'money\': " + str(bal) + "}]}"
        return bankworld_pb2.BranchReply(branch_msg=branchmsg)


