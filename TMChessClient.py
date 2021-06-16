from member_data_layer.chess import Member
from network_client.client import NetworkClient
from network_common.wrappers import *
import sys
import tkinter

class ListBox():
 def __init__(self,master,activated):
  self.master=master
  self.activated=activated
  self.lastSelectedRowRectangle=None
  self.inviteIcon=tkinter.PhotoImage(file="images\\invite.png")
  self.inviteClickedIcon=tkinter.PhotoImage(file="images\\invite_clicked.png")
  self.invitationSentIcon=tkinter.PhotoImage(file="images\\invitation_sent_icon.png")
  self.invitationSentClickedIcon=tkinter.PhotoImage(file="images\\invitation_sent_clicked_icon.png")
  self.update()
 
 def update(self):
  if not self.activated: return
  self.master.canvas.create_rectangle(605,51,748,648,width=1)
  self.master.canvas.create_text(622,52,text="Available Users",anchor='nw',font=("Comic Sans MS",11,"bold"))
  difference=0
  for username,value in self.master.availableUsers.items():  
   self.master.canvas.create_text(610,85+difference,text=username,anchor='nw')
   if value["invitation_status"]:self.master.canvas.create_image(720,80+difference,anchor='nw',image=self.invitationSentIcon)
   else: self.master.canvas.create_image(720,80+difference,anchor='nw',image=self.inviteIcon)
   if value["selected"]: 
    self.lastSelectedRowRectangle=self.master.canvas.create_rectangle(value["coordinates"],outline="#F29C1F",width=1)
   difference+=24
 
 def mouseMoved(self,x,y):
  if(self.lastSelectedRowRectangle is not None): self.master.canvas.delete(self.lastSelectedRowRectangle)
  if x>=607 and x<=746:
   yc=80
   for value in self.master.availableUsers.values():
    value["selected"]=False
    value["coordinates"]=None
    if y>=yc and y<=yc+23:
     value["selected"]=True
     value["coordinates"]=(607,yc,746,yc+24)
     self.lastSelectedRowRectangle=self.master.canvas.create_rectangle(607,yc,746,yc+24,outline="#F29C1F",width=1)
    yc+=24

 def listBoxClicked(self,x,y):
  if x>=720 and x<=744:
   yc=80
   for user,value in self.master.availableUsers.items():
    if y>=yc and y<=yc+24:
     if not value["invitation_status"]: value["invitation_status"]=True
     self.onInviteButtonClicked(user,value["invitation_status"],720,yc)
     value["selected"]=True
     break
    yc+=24
 
 def onInviteButtonClicked(self,username,invitation_status,x,y):
  print(f"onInviteButtonClicked got called, invited : {username}")
  if invitation_status: self.master.canvas.create_image(x,y,anchor='nw',image=self.invitationSentClickedIcon)
  else: self.master.canvas.create_image(x,y,anchor='nw',image=self.inviteClickedIcon)
  self.master.after(100,self.master.setIcon(x,y,self.invitationSentIcon))
 
class InvitationPanel:
 def __init__(self,master,activated):
  self.master=master
  self.activated=activated
  self.lastSelectedRowRectangle=None
  self.coordinatesOfLastRectangle=None
  self.acceptIcon=tkinter.PhotoImage(file="images\\accept.png")
  self.declineIcon=tkinter.PhotoImage(file="images\\decline.png")
  self.acceptClickedIcon=tkinter.PhotoImage(file="images\\accept2.png")
  self.declineClickedIcon=tkinter.PhotoImage(file="images\\decline2.png")
  self.closeIcon=tkinter.PhotoImage(file="images\\close.png")
  self.closeClickedIcon=tkinter.PhotoImage(file="images\\close_clicked.png")
  self.update()
  
 def mouseMoved(self,x,y):
  if(self.lastSelectedRowRectangle is not None): self.master.canvas.delete(self.lastSelectedRowRectangle)
  if x>=10 and x<=594:
   yc=103
   length=len(self.master.usersInvitedYou)
   i=0
   while i<length:
    if y>=yc and y<=yc+35: 
     self.coordinatesOfLastRectangle=(10,yc,594,yc+35)
     self.lastSelectedRowRectangle=self.master.canvas.create_rectangle(self.coordinatesOfLastRectangle,outline="#505050",width=1)
     break
    yc+=40
    i+=1
   else:
    self.coordinatesOfLastRectangle=None

 def invitationPanelClicked(self,x,y):
  length=len(self.master.usersInvitedYou)
  if x>=365 and x<=397:  # for accept
   yc=105
   for i in range(length):
    if y>=yc and y<=yc+32:
     self.onAcceptButtonClicked(i,365,yc)
     break
    yc+=40
  elif x>=510 and x<=542:  # for decline
   yc=105
   for i in range(length):
    if y>=yc and y<=yc+32:
     self.onDeclineButtonClicked(i,510,yc)
     break
    yc+=40
  elif x>=581 and x<=603 and y>=50 and y<=72:
   self.onInvitationPanelCloseButtonClicked()
  
 def onAcceptButtonClicked(self,row,x,y):
  print(f"onAcceptButtonClicked got called, accepted invitation of {self.master.usersInvitedYou[row]}")
  self.master.canvas.create_image(x,y,anchor='nw',image=self.acceptClickedIcon)
  self.master.after(100,self.master.setIcon(x,y,self.acceptIcon))

 def onDeclineButtonClicked(self,row,x,y):
  print(f"onDeclineButtonClicked got called, declined invitation of {self.master.usersInvitedYou[row]}")
  self.master.canvas.create_image(x,y,anchor='nw',image=self.declineClickedIcon)
  #self.master.usersInvitedYou.pop(row)
  self.master.after(100,self.setDeclineIcon(x,y,self.declineIcon))
  
 def setDeclineIcon(self,xcor,ycor,icon):
  def f():
   self.master.canvas.create_image(xcor,ycor,image=icon,anchor='nw')
   self.master.canvas.delete('all')
   self.master.updateBoard()
  return f

 def onInvitationPanelCloseButtonClicked(self):
  print("onInvitationPanelCloseButtonClicked got called")
  self.activated=False
  self.master.canvas.create_image(581,50,anchor='nw',image=self.closeClickedIcon)
  self.master.canvas.create_text(589,50,text="X",anchor='nw',fill='white',font=12)
  self.master.after(100,self.master.updateBoard)
 
 def update(self):
  if not self.activated: return
  self.lastUpdated=self.master.canvas.create_rectangle(3,50,602,649,width=1,fill="white",outline="#505050")
  self.master.canvas.create_line(3,100,602,100,fill="#505050")
  self.master.canvas.create_line(310,50,310,650,fill="#505050")
  self.master.canvas.create_line(455,100,455,650,fill="#505050")
  self.master.canvas.create_text(100,55,text="MEMBER",anchor='nw',font=("Comic Sans MS",20),fill='#484848')
  self.master.canvas.create_text(400,55,text="ACTION",anchor='nw',font=("Comic Sans MS",20),fill="#484848")
  self.master.canvas.create_image(581,50,anchor='nw',image=self.closeIcon)
  self.master.canvas.create_text(589,50,text="X",anchor='nw',fill='white',font=12)
  length=len(self.master.usersInvitedYou)
  difference=0
  i=0
  while i<length:
   self.master.canvas.create_text(40,110+difference,text=f"{i+1}.",anchor='ne',font=("Comic Sans MS",14),fill="#484848")
   self.master.canvas.create_text(45,110+difference,text=self.master.usersInvitedYou[i],anchor='nw',font=("Comic Sans MS",14),fill="#484848")
   self.master.canvas.create_image(365,105+difference,image=self.acceptIcon,anchor='nw')
   self.master.canvas.create_image(510,105+difference,image=self.declineIcon,anchor='nw')
   difference+=40
   i+=1
  if self.coordinatesOfLastRectangle: 
   self.lastSelectedRowRectangle=self.master.canvas.create_rectangle(self.coordinatesOfLastRectangle,outline="#505050",width=1)
   
class ChessBoard(tkinter.Tk):
 def __init__(self,member):
  tkinter.Tk.__init__(self)
  self.title(f"Chess : The Game")
  self.geometry("753x653")
  self.canvas=tkinter.Canvas(master=self,width=750,height=650,bg='white')
  self.canvas.grid(row=0,column=0)
  self.canvas.bind("<Button-1>",self.onChessBoardClicked)
  self.canvas.bind("<Motion>",self.onMouseMoved)
  self.board=self.createBoardDataStructure()
  self.member=member
  self.availableUsers={}
  self.usersInvitedYou=[]
  self.usersInvitedYou=["Amit","Bobby","Sohan","Rohit"]
  self.listBox=ListBox(self,True)
  self.invitationPanel=InvitationPanel(self,False)
  self.invitationsIcon=tkinter.PhotoImage(file="images\\invitations_icon.png")
  self.invitationsIconClicked=tkinter.PhotoImage(file="images\\invitations_icon_clicked.png")
  #self.loadPieces()
  #self.initializeNewGame()
  self.updateBoard()
  self.getAvailableUsers()

 def updateBoard(self):
  self.canvas.delete('all')
  self.canvas.create_text(8,8,anchor='nw',text=self.member.username,fill='darkred',font=("Comic Sans MS",18))
  self.canvas.create_rectangle(2,2,750,650,width=1)
  self.canvas.create_line(2,49,750,49)
  self.canvas.create_line(603,50,603,650)
  self.canvas.create_image(712,10,anchor='nw',image=self.invitationsIcon)
  length=len(self.usersInvitedYou)
  x=733
  if(length>9): x=740
  self.canvas.create_text(x,13,text=f"{length}",anchor='ne',fill='white',font=("Comic Sans MS",14))
  self.listBox.update()
  self.invitationPanel.update()
  if self.invitationPanel.activated: return  
  ycor=50
  for x in range(8): 
   xcor=3
   for y in range(8):
    if y%2==0:
     if x%2==0:
      self.canvas.create_rectangle(xcor,ycor,xcor+75,ycor+75,fill="#FFFFFF",width=0)  # width=0 for width of border should be zero
     else:
      self.canvas.create_rectangle(xcor,ycor,xcor+75,ycor+75,fill="#FF0000",width=0)
    else:
     if x%2==0:
      self.canvas.create_rectangle(xcor,ycor,xcor+75,ycor+75,fill="#FF0000",width=0)
     else:
      self.canvas.create_rectangle(xcor,ycor,xcor+75,ycor+75,fill="#FFFFFF",width=0)
    if self.board[x][y]!=None:
     self.canvas.create_image(xcor,ycor,image=self.pieces[self.board[x][y]],anchor='nw')
    xcor+=75
   ycor+=75 
 
 def onMouseMoved(self,event):
  x=event.x
  y=event.y
  if x>=605 and x<=748 and y>=51 and y<=648:
   self.listBox.mouseMoved(x,y)
  elif self.invitationPanel.activated and x>=3 and x<=602 and y>=50 and y<=649:
   self.invitationPanel.mouseMoved(x,y)

 def onChessBoardClicked(self,event):
  #print(f"({event.x},{event.y})")
  x=event.x
  y=event.y
  if x>=605 and x<=748 and y>=51 and y<=648:
   self.listBox.listBoxClicked(x,y)
  elif x>=712 and x<=744 and y>=10 and y<=42 :
   self.onInvitationsIconClicked()
  elif x>=2 and x<=602 and y>=50 and y<=649:
   if self.invitationPanel.activated:
    self.invitationPanel.invitationPanelClicked(x,y)
   else: 
    row=self.getBoardY(y)
    column=self.getBoardX(x)
    print(f"({row},{column})")

 def onInvitationsIconClicked(self):
  print("onInvitationsIconClicked got called")
  self.invitationPanel.activated=True
  self.canvas.create_image(712,10,anchor='nw',image=self.invitationsIconClicked)
  length=len(self.usersInvitedYou)
  x=733
  if(length>9): x=740
  self.canvas.create_text(x,13,text=length,anchor='ne',fill='white',font=("Comic Sans MS",14))
  self.invitationPanel.update()
  self.after(100,self.updateBoard)

 def setIcon(self,xcor,ycor,icon):
  def f():
   self.canvas.create_image(xcor,ycor,image=icon,anchor='nw')
  return f

 def createBoardDataStructure(self):
  board=[]
  for x in range(8):
   to_append=[]
   for y in range(8):
    to_append.append(None)
   board.append(to_append)
  return board

 def loadPieces(self):
  self.pieces={}
  self.pieces["wp"]=tkinter.PhotoImage(file="wp.png")
  self.pieces["wr"]=tkinter.PhotoImage(file="wr.png")
  self.pieces["wkt"]=tkinter.PhotoImage(file="wkt.png")
  self.pieces["wb"]=tkinter.PhotoImage(file="wb.png")
  self.pieces["wk"]=tkinter.PhotoImage(file="wk.png")
  self.pieces["wq"]=tkinter.PhotoImage(file="wq.png")
  self.pieces["bp"]=tkinter.PhotoImage(file="bp.png")
  self.pieces["br"]=tkinter.PhotoImage(file="br.png")
  self.pieces["bkt"]=tkinter.PhotoImage(file="bkt.png")
  self.pieces["bb"]=tkinter.PhotoImage(file="bb.png")
  self.pieces["bk"]=tkinter.PhotoImage(file="bk.png")
  self.pieces["bq"]=tkinter.PhotoImage(file="bq.png")

 def initializeNewGame(self):
  self.board[0][0]="wr"
  self.board[0][1]="wkt"
  self.board[0][2]="wb"
  self.board[0][3]="wk"
  self.board[0][4]="wq"
  self.board[0][5]="wb"
  self.board[0][6]="wkt"
  self.board[0][7]="wr"
  self.board[1][0]="wp"
  self.board[1][1]="wp"
  self.board[1][2]="wp"
  self.board[1][3]="wp"
  self.board[1][4]="wp"
  self.board[1][5]="wp"
  self.board[1][6]="wp"
  self.board[1][7]="wp"
  self.board[6][0]="bp"
  self.board[6][1]="bp"
  self.board[6][2]="bp"
  self.board[6][3]="bp"
  self.board[6][4]="bp"
  self.board[6][5]="bp"
  self.board[6][6]="bp"
  self.board[6][7]="bp"
  self.board[7][0]="br"
  self.board[7][1]="bkt"
  self.board[7][2]="bb"
  self.board[7][3]="bk"
  self.board[7][4]="bq"
  self.board[7][5]="bb"
  self.board[7][6]="bkt"
  self.board[7][7]="br"

 def getBoardX(self,mouseX):
  xc=2
  for x in range(8):
   if mouseX>=xc and mouseX<=xc+74: return x
   xc+=75  
  return -1

 def getBoardY(self,mouseY):
  yc=50
  for y in range(8):
   if mouseY>=yc and mouseY<=yc+74: return y
   yc+=75  
  return -1

 def getAvailableUsers(self):
  request=Request(manager='ChessBoardManager',action='getAvailableUsers')
  response=network_client.send(request)  
  availableUsers=Wrapper.fromJSON(response.result_json_string)
  availableUsers.remove(self.member.username)
  temp={}
  for username in availableUsers:
   if username not in self.availableUsers:
    temp[username]={"invitation_status":False,"selected":False,"coordinates":None}
   else:
    temp[username]=self.availableUsers[username]
  self.availableUsers=temp
  self.updateBoard()
  self.after(2000,self.getAvailableUsers)

 def destroy(self):
  request=Request(manager='ChessBoardManager',action='logout',request_object=Member(self.member.username,""))
  response=network_client.send(request)
  super().destroy()

length=len(sys.argv)
if length==1 or length>3: 
 print("Please provide username and password only")
 sys.exit()
member=Member(sys.argv[1],sys.argv[2])
network_client=NetworkClient()
request=Request(manager='ChessBoardManager',action='authenticate',request_object=member)
response=network_client.send(request)
if not response.success:
 print("Invalid Username / Password");
 sys.exit()
cb=ChessBoard(member)
cb.mainloop()
