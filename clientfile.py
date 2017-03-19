#-*- coding:utf-8 -*-  

import emoji
import Tkinter
import tkFont,socket, thread,threading
import time
import sys
import string
import select
import struct

class ClientUI():
    title = 'Python Chatting- Client-v1.0'
    local = '127.0.0.1'
    port = 5000
    global clientSock
    def __init__(self):
        self.change=0
        self.root = Tkinter.Tk()
        self.root.title(self.title)
        
        self.frame = [Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame()]

        self.chatTextScrollBar = Tkinter.Scrollbar(self.frame[0])
        self.chatTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)
        
        ft = tkFont.Font(family='Fixdsys',size=11)
        self.chatText = Tkinter.Listbox(self.frame[0],width=70,height=18,bg='lightyellow2',font=ft)
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set
        self.chatText.pack(expand=1,fill=Tkinter.BOTH)
        self.chatTextScrollBar['command'] = self.chatText.yview()
        self.frame[0].pack(expand=1,fill=Tkinter.BOTH)
        
        label = Tkinter.Label(self.frame[1],height=2)
        label.pack(fill=Tkinter.BOTH)
        self.frame[1].pack(expand=1,fill=Tkinter.BOTH)
        
        self.inputTextScrollBar = Tkinter.Scrollbar(self.frame[2])
        self.inputTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)
        
        self.inputText = Tkinter.Text(self.frame[2],width=70,height=8,bg='burlywood1',font=ft)
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set
        self.inputText.pack(expand=1,fill=Tkinter.BOTH)
        self.inputTextScrollBar['command'] = self.chatText.yview()
        self.frame[2].pack(expand=1,fill=Tkinter.BOTH)
        
        self.inputText.bind("<Return>", self.textChange)
        self.inputText.focus_set()
        
        self.sendButton=Tkinter.Button(self.frame[3],text=' 发 送 ',width=10,command=self.sendMessage)
        self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.RIGHT,padx=15,pady=8)

       
        self.closeButton=Tkinter.Button(self.frame[3],text=' 关 闭 ',width=10,command=self.close)
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)
    def textChange(self,event):
        sys.stdout.write(self.inputText.get('1.0',Tkinter.END))
        sys.stdout.flush()
          
    def receiveMessage(self):
        self.clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        self.clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientSock.settimeout(2)
        try:
            self.clientSock.connect((self.local, self.port))
        except:
            print '无法连接'
            self.chatText.insert(Tkinter.END,'无法连接，请检查服务器端是否已经启动')
            return
        
        print emoji.emojize('成功连接. 开始聊天吧:smile:', use_aliases=True)

        sys.stdout.flush()
        self.chatText.insert(Tkinter.END,'成功连接. 开始聊天吧')
        self.buffer = 4096
      
        while True:
           
            self.rlist=[sys.stdout,self.clientSock]
            self.read_list, self.write_list,self.error_list = select.select(self.rlist , [], [])
            for self.sock in self.read_list:
                if self.sock==self.clientSock:
                    self.data=self.sock.recv(self.buffer)
                    if not self.data:
                        print '\n无法连接服务器'
                        self.chatText.insert(Tkinter.END,'\n无法连接服务器')
                        sys.exit()
        
                    else:
                        self.chatText.insert(Tkinter.END, self.data)  
                else:
                    self.sendMessage()
 
    def sendMessage(self):
        msg=self.inputText.get('1.0',Tkinter.END)
        theTime=time.strftime("\t%Y-%m-%d %H:%M:%S",time.localtime())
        self.chatText.insert(Tkinter.END,'< Me >'+ theTime +' 说：\n')
        self.chatText.insert(Tkinter.END,'  ' +msg + '\n')
        self.clientSock.send(msg)
        self.inputText.delete(0.0,msg.__len__()-1.0)
    def close(self):
        sys.exit()
    
    def startNewThread(self):   
        thread.start_new_thread(self.receiveMessage,())

def main():
    client = ClientUI()
    client.startNewThread()
    client.root.mainloop()
    
if __name__=='__main__':
    reload(sys)  
    sys.setdefaultencoding('utf8')
    main()

