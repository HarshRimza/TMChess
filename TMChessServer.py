from network_server.server import NetworkServer
from network_common.wrappers import *
from member_data_layer.chess import *

class Members:
 def __init__(self):
  self.members=[]
  self.members.append(Member("amit","amit"))
  self.members.append(Member("bobby","bobby"))
  self.members.append(Member("raju","raju"))
  self.members.append(Member("sonu","sonu"))
  self.members.append(Member("bholu","bholu"))
  self.members.append(Member("gopal","gopal"))
  self.members.append(Member("garima","garima"))  
 def getMembers(self):
  return self.members

class TMChessServer():
 _members=None
 def __init__(self):
  self.logged_in_users=set()
  self.playing_users=set()
  if TMChessServer._members==None:
   m=Members()
   members={}
   for member in m.getMembers():
    members[member.username]=member
   TMChessServer._members=members

 def start(self):
  networkServer=NetworkServer(self)
  networkServer.start()

 def authenticate(self,member):
  if (member.username in TMChessServer._members) and (member.username not in self.logged_in_users):
   if member.password==TMChessServer._members[member.username].password:
    self.logged_in_users.add(member.username)
    return True
  return False

 def logout(self,member):
  self.logged_in_users.discard(member.username)
  print(self.logged_in_users)
 
 def getAvailableUsers(self):
  return list(self.logged_in_users.difference(self.playing_users))

 def __call__(self,request):
  if request.manager=="ChessBoardManager":
   if request.action=="authenticate":
    print(f"action : authenticate, json : ({request.json_string})")
    decision=self.authenticate(Member.fromJSON(request.json_string))
    response=Response(success=decision)
    return response
   if request.action=="getAvailableUsers":
    print(f"action : getAvailableUsers, json : ({request.json_string})")
    response=Response(success=True,result_object=Wrapper(self.getAvailableUsers()))
    return response
   if request.action=="logout":
    print(f"action : logout, json : ({request.json_string})")
    self.logout(Member.fromJSON(request.json_string))
    response=Response(success=True)
    return response


tmChessServer=TMChessServer()
tmChessServer.start()
