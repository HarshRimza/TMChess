import tkinter
class ChessBoard(tkinter.Tk):
 def __init__(self):
  tkinter.Tk.__init__(self)
  self.geometry("700x700")
  self.canvas=tkinter.Canvas(master=self,width=600,height=600)
  self.canvas.grid(row=0,column=0)
  self.board=self.createBoardDataStructure()
  self.loadPieces()
  self.initializeNewGame()
  self.updateBoard()
  self.canvas.bind("<Button-1>",self.onChessBoardClicked)
  

 def createBoardDataStructure(self):
  board=[]
  for x in range(8):
   board.append([])
   for y in range(8):
    board[x].append(None)
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

 def updateBoard(self):
  ycor=0
  for x in range(8):
   xcor=0
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
 
 def onChessBoardClicked(self,event):
  #print(f"({event.x},{event.y})")
  row=self.getBoardY(event.y)
  column=self.getBoardX(event.x)
  print(f"({row},{column})")

 def getBoardX(self,mouseX):
  xc=0
  for x in range(8):
   if mouseX>=xc and mouseX<=xc+74: return x
   xc+=75  
  return -1

 def getBoardY(self,mouseY):
  yc=0
  for y in range(8):
   if mouseY>=yc and mouseY<=yc+74: return y
   yc+=75  
  return -1





cb=ChessBoard()
cb.mainloop()