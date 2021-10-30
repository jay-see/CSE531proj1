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

    def createStubsss(self, branches):
        print ("Number of BRANCHES is "+ str(branches))
        for i in range(branches):
            if (i+1) != self.id :
                channelnumber = 50050+i+1
                channel = grpc.insecure_channel('localhost:'+str(channelnumber))
                self.stubList.append(bankworld_pb2_grpc.BranchStub(channel))
                print ("Created BRANCH stub " + str(channelnumber))
            else :
                self.stubList.append(None)
        return ("Done creating BRANCH stubsss!!")

    def Propagate_Deposit(self, amount, context):
        new_bal = self.balance + int(amount.msg)
        print ("PROPAGATING DEPOSIT TO BRANCH #"+str(self.id)+".NEW BALANCE IS "+str(new_bal))
        if new_bal >= 0:
            self.balance = new_bal
            print ("NEW BRANCH BALANCE = "+str(self.balance))
            depositmsg = "success"
        else :
            depositmsg = "fail"
        return bankworld_pb2.DepositReply(deposit_msg=depositmsg)
    
    def Propagate_Withdraw(self, amount, context):
        new_bal = self.balance - int(amount.msg)
        print ("PROPAGATING WITHDRAW TO BRANCH #"+str(self.id)+".NEW BALANCE IS "+str(new_bal))
        if new_bal >= 0:
            self.balance = new_bal
            print ("NEW BRANCH BALANCE = "+str(self.balance))
            withdrawmsg = "success"
        else :
            withdrawmsg = "fail"
        return bankworld_pb2.WithdrawReply(withdraw_msg=withdrawmsg)
    
    def Query(self):
        return self.balance
    
    def Deposit(self, amount):
        new_bal = self.balance + amount
        if new_bal >= 0:
            self.balance = new_bal
            print(str(self.id)+"PROPAGATING deposit\n"+str(self.stubList))
            for i in range(len(self.stubList)) :
                if (i+1) != self.id :
                    response = self.stubList[i].Propagate_Deposit(bankworld_pb2.DepositRequest(msg=str(amount)))
            print("Customer received: " + response.deposit_msg)
            return (response.deposit_msg)
        else:
            return "fail"

    def Withdraw(self, amount):
        new_bal = self.balance - amount
        if new_bal >= 0:
            self.balance = new_bal
            print(str(self.id)+"PROPAGATING withdraw\n"+str(self.stubList))
            for i in range(len(self.stubList)) :
                if (i+1) != self.id :
                    response = self.stubList[i].Propagate_Withdraw(bankworld_pb2.WithdrawRequest(msg=str(amount)))
            print("Customer received: " + response.withdraw_msg)
            return (response.withdraw_msg)
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
                print("WITHDRAW"+str(self.id))
                result = Branch.Withdraw(self,i['money'])
                branchmsg = branchmsg + "\'" + result + "\'}, {\'interface\': "
            elif i['interface'] == 'query':
#                time.sleep(3)
                bal = Branch.Query(self)
                branchmsg = branchmsg + "\'query\', \'result\': 'success', \'money\': "  # leave out balance until the end of program
        return bankworld_pb2.BranchReply(branch_msg=branchmsg)


