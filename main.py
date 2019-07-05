# coding: utf-8 
import tkinter
import random

class Field():
    def __init__(self,x,y,mine):
        
        self.x = x
        self.y = y
        self.start_mine = mine

        #ゲームが終わったかどうか
        self.game_finish = False

        self.nomal_color = "gray"
        self.flag_color = "lightskyblue"
        self.enter_color = "lightgray"

        self.main = tkinter.Tk()
        self.main.title(u"マインスイーパー")
        #self.main.geometry( str(self.x * 40 + 20) + "x" +  str(self.y * 40 + 170) )
        
        self.main.grid_columnconfigure((0,1,2),weight=1)

        self.message_mine = tkinter.IntVar()
        tkinter.Label(master=self.main,font=("",20),bd=1,fg = "red",textvariable= self.message_mine).pack(pady = 0)
        
        self.message_time = tkinter.StringVar()
        tkinter.Label(master=self.main,font=("",20),textvariable= self.message_time).pack(pady = 0)

        tkinter.Button(master=self.main,text=u"リセット",command=self.Reset).pack(pady = 0)
        
        self.message_game = tkinter.StringVar()
        tkinter.Label(master=self.main,font=("",20),textvariable= self.message_game).pack(pady = 0)

        self.canvas = tkinter.Canvas(master=self.main,width = self.x * 40 + 20, height = self.y * 40 + 20)
        self.canvas.pack()

        self.Game_Init()

        self.canvas.after(1000,self.Loop)

    def Bopen(self,ev):
        if self.canvas.itemconfig("current")["fill"][4] == self.flag_color:
            return

        map_data = self.canvas.gettags("current")[0].split("-")
        self.active_field -= 1
        self.canvas.delete("current")

        if self.Mine_map[ int( map_data[1] ) ][ int( map_data[2] ) ] == 0:
            self.Copen( int( map_data[1] ) , int( map_data[2] ) )
        elif self.Mine_map[ int( map_data[1] ) ][ int( map_data[2] ) ] == 9:
            self.Gameover("bomb")

        if self.active_field - self.start_mine == 0:
            self.Gameover("clear")


    def Copen(self,y,x):
        if x > 0:
            Next_map = self.canvas.gettags( "field-" + str(y) + "-" + str(x-1) )

            if not( Next_map == () ) and not(self.Mine_map[y][x-1] == 9):
                self.active_field -= 1
                self.canvas.delete(Next_map)
                if self.Mine_map[y][x-1] == 0:
                    self.Copen(y,x-1)

        if x < self.x - 1:
            Next_map = self.canvas.gettags( "field-" + str(y) + "-" + str(x+1) )

            if not( Next_map == () ) and not(self.Mine_map[y][x+1] == 9):
                self.active_field -= 1
                self.canvas.delete(Next_map)
                if self.Mine_map[y][x+1] == 0:
                    self.Copen(y,x+1)
        
        if y > 0:
            Next_map = self.canvas.gettags( "field-" + str(y-1) + "-" + str(x) )

            if not( Next_map == () ) and not(self.Mine_map[y-1][x] == 9):
                self.active_field -= 1
                self.canvas.delete(Next_map)
                if self.Mine_map[y-1][x] == 0:
                    self.Copen(y-1,x)
        
        if y < self.y - 1:
            Next_map = self.canvas.gettags( "field-" + str(y+1) + "-" + str(x) )

            if not( Next_map == () ) and not(self.Mine_map[y+1][x] == 9):
                self.active_field -= 1
                self.canvas.delete(Next_map)
                if self.Mine_map[y+1][x] == 0:
                    self.Copen(y+1,x)

        

    def Enter(self,ev):
        if self.canvas.itemconfig("current")["fill"][4] == self.nomal_color:
            self.canvas.itemconfigure("current" , fill = self.enter_color)
        

    def Fadd(self,y,x):

        if y > 0:
            self.Mine_map[y-1][x] = self.Mine_map[y-1][x] + 1 if not(self.Mine_map[y-1][x] == 9) else self.Mine_map[y-1][x] 
            
        if y < self.y - 1:
            self.Mine_map[y+1][x] = self.Mine_map[y+1][x] + 1 if not(self.Mine_map[y+1][x] == 9) else self.Mine_map[y+1][x]

        if x > 0:
            self.Mine_map[y][x-1] = self.Mine_map[y][x-1] + 1 if not(self.Mine_map[y][x-1] == 9) else self.Mine_map[y][x-1]

        if x < self.x - 1:
            self.Mine_map[y][x+1] = self.Mine_map[y][x+1] + 1 if not(self.Mine_map[y][x+1] == 9) else self.Mine_map[y][x+1]

        if x > 0 and y > 0:
            self.Mine_map[y-1][x-1] = self.Mine_map[y-1][x-1] + 1 if not(self.Mine_map[y-1][x-1]== 9) else self.Mine_map[y-1][x-1]
        
        if x > 0 and y < self.y - 1:
            self.Mine_map[y+1][x-1] = self.Mine_map[y+1][x-1] + 1 if not(self.Mine_map[y+1][x-1] == 9) else self.Mine_map[y+1][x-1]

        if y > 0 and x < self.x - 1:
            self.Mine_map[y-1][x+1] = self.Mine_map[y-1][x+1] + 1 if not(self.Mine_map[y-1][x+1] == 9) else self.Mine_map[y-1][x+1]

        if x < self.x - 1 and y < self.y - 1:
            self.Mine_map[y+1][x+1] = self.Mine_map[y+1][x+1] + 1 if not(self.Mine_map[y+1][x+1] == 9) else self.Mine_map[y+1][x+1]

    def Field_init(self):

        self.Field_tag = []        

        for lop in range(self.y):
            Tbuf = []

            for lop2 in range(self.x):
                Mtag = "field-" + str(lop) + "-" + str(lop2)
                Tbuf.append( Mtag )
                self.canvas.create_rectangle(lop2 * 40 + 10, lop * 40 + 10, lop2 * 40 + 50, lop * 40 + 50,tag = Mtag , fill = self.nomal_color , outline = "white" , width = 2)
                self.canvas.tag_bind(Mtag , "<Button-1>" , self.Bopen)
                self.canvas.tag_bind(Mtag , "<Button-3>" , self.Flag)
                self.canvas.tag_bind(Mtag , "<Enter>" , self.Enter)
                self.canvas.tag_bind(Mtag , "<Leave>" , self.Leave)

            self.Field_tag.append(Tbuf)

    def Flag(self,ev):
        if self.canvas.itemconfig("current")["fill"][4] == self.enter_color:
            self.canvas.itemconfigure("current" , fill = self.flag_color)

            mine = self.message_mine.get()
            self.message_mine.set( mine - 1 )
        else:
            self.canvas.itemconfigure("current" , fill = self.enter_color)

            mine = self.message_mine.get()
            self.message_mine.set( mine + 1 )

    def Game_Init(self):
        
        self.canvas.create_rectangle(0,0,self.x * 40 + 20, self.y * 40 + 20, fill = "white")
        self.message_game.set(u"")
        self.message_mine.set(self.start_mine)

        self.active_field = self.x * self.y

        self.Mine_set()
        self.Map_load()
        self.Field_init()

        if self.game_finish == True:
            self.game_finish = False
            self.canvas.after(1000,self.Loop)
            
        self.message_time.set(u"time 0 : 00")
        self.time = 0

        

    def Gameover(self,res):
        
        if res == "clear":
            self.message_game.set(u"ゲームクリア")
        elif res == "bomb":
            self.message_game.set(u"ボムりました")
        
        for lop in range(self.y):
            for lop2 in range(self.x):
                Mtag = "field-" + str(lop) + "-" + str(lop2)

                if not(self.canvas.gettags( Mtag ) == () ):

                    if self.Mine_map[lop][lop2] == 9:

                        if self.canvas.itemconfig(Mtag)["fill"][4] == self.flag_color:
                            self.canvas.tag_raise("map-" + str(lop) + "-" + str(lop2))
                        else:
                            self.canvas.delete(Mtag)

                    self.canvas.tag_unbind(Mtag , "<Button-1>")
                    self.canvas.tag_unbind(Mtag , "<Button-3>")
                    self.canvas.tag_unbind(Mtag , "<Enter>")
                    self.canvas.tag_unbind(Mtag , "<Leave>")
        self.game_finish = True

    def Leave(self,ev):
        if self.canvas.itemconfig("current")["fill"][4] == self.enter_color:
            self.canvas.itemconfigure("current" , fill = self.nomal_color)

    def Loop(self):
        if self.game_finish:
            return

        self.time += 1
        message = u"time " + str( int( (self.time - (self.time % 60) ) / 60 ) ) + " : "
        if self.time % 60 < 10:
            message += u"0" + str(self.time % 60)
        else:
            message +=  str( self.time % 60)
        self.message_time.set( message )

        self.canvas.after(1000,self.Loop)

    def Map_load(self):
        num_color = ["","black","midnightblue","blue","darkturquoise","darkgreen","green","orange","blueviolet","red"]

        for lop in range(len(self.Mine_map)):

            for lop2 in range(len(self.Mine_map[0])):
                Mtag = "map-" + str(lop) + "-" + str(lop2)
                
                if self.Mine_map[lop][lop2] == 9:
                    self.canvas.create_text(lop2 * 40 + 30 , lop * 40 + 30,tag = Mtag ,font = ("",20),text = "B" , fill = num_color[self.Mine_map[lop][lop2]])
                elif self.Mine_map[lop][lop2] > 0:
                    self.canvas.create_text(lop2 * 40 + 30 , lop * 40 + 30,tag = Mtag ,font = ("",20),text = str(self.Mine_map[lop][lop2]) , fill = num_color[self.Mine_map[lop][lop2]])
                

    def Mine_set(self):
        self.Mine_map = []
        Mine_place = sorted( random.sample( range(self.x * self.y) , self.start_mine ) ) 
        cnt = 0

        for lop in range(self.y):
            buf = []
            for lop2 in range(self.x):
                if len(Mine_place) > 0 and Mine_place[0] == cnt :
                    del Mine_place[0]
                    buf.append(9)
                else:
                    buf.append(0)
                cnt += 1
            self.Mine_map.append(buf)
             
        for lop in range(self.y):
            for lop2 in range(self.x):
                if self.Mine_map[lop][lop2] == 9:
                    self.Fadd(lop,lop2)

    def Reset(self):
        self.canvas.delete("all")
        
        self.Game_Init()



def set_func():

    if size_x.get().isdecimal() == False or size_y.get().isdecimal() == False or mine_num.get().isdecimal() == False:
        message_err.set(u"文字や負数を入れるな")
        return
    x = int(size_x.get())
    y = int(size_y.get())
    mine = int(mine_num.get())

    if x < 4 or y < 4 or mine < 1:
        message_err.set(u"少ない")

    #マス数*0.8　まで許容
    elif x > 20 or y > 20 or x * y  < int( mine / 0.8 ) :
        message_err.set(u"多い")

    else:
        config.destroy()
        
        game = Field(x,y,mine)
        game.main.mainloop()

config = tkinter.Tk()
config.title("config")

tkinter.Label(master=config,text=u"サイズ").grid(row = 0,column = 0)

size_x = tkinter.Entry(master=config)
size_x.insert(tkinter.END,u"12")
size_x.grid(row = 0,column = 1)

tkinter.Label(master=config,text="×").grid(row = 0,column = 2)

size_y = tkinter.Entry(master=config)
size_y.insert(tkinter.END,u"8")
size_y.grid(row = 0,column = 3)

tkinter.Label(master=config,text=u"地雷数").grid(row = 1,column = 0)

mine_num = tkinter.Entry(master=config)
mine_num.insert(tkinter.END,u"10")
mine_num.grid(row = 1,column = 1)

tkinter.Button(master=config,text=u"スタート",command=set_func).grid(row=2,columnspan=3)

message_err = tkinter.StringVar()
tkinter.Label(master=config,textvariable=message_err).grid(row = 3,columnspan=3)

config.mainloop()