# -*- coding: UTF-8 -*-
import emoji
import Tkinter,socket,thread,sys,select
import tkFont  
import time
import os
import struct

class ServerUI():
    title = 'Python Chatting- Server-v1.0'
    local= '127.0.0.1'  
    port = 5000     
    global serverSock 
    global CONNECTION_LIST
    def __init__(self):
        self.CONNECTION_LIST= []
        self.root = Tkinter.Tk()  
        self.root.title(self.title)  

        self.frame = [Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame()]  
         
        self.chatTextScrollBar = Tkinter.Scrollbar(self.frame[0])  
        self.chatTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)  
                   
        ft = tkFont.Font(family='Fixdsys',size=11)  
        self.chatText = Tkinter.Listbox(self.frame[0],width=70,height=18,font=ft)  
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set  
        self.chatText.pack(expand=1,fill=Tkinter.BOTH)  
        self.chatTextScrollBar['command'] = self.chatText.yview()  
        self.frame[0].pack(expand=1,fill=Tkinter.BOTH)           
         
        label = Tkinter.Label(self.frame[1],height=2)  
        label.pack(fill=Tkinter.BOTH)  
        self.frame[1].pack(expand=1,fill=Tkinter.BOTH)  
       
        self.closeButton=Tkinter.Button(self.frame[2],text=' 关 闭 ',width=10,command=self.close)  
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=25,pady=5)  
        self.frame[2].pack(expand=1,fill=Tkinter.BOTH)
    
    def receiveMessage(self):
        # Start a new socket
        self.serverSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSock.bind((self.local,self.port)) #127.0.0.1:5000
        self.serverSock.listen(15)  
        self.buffer = 4096  
        self.chatText.insert(Tkinter.END,'服务器已经就绪......')
        self.CONNECTION_LIST.append(self.serverSock)
        
        print "聊天服务器工作端口：" + str(self.port)
        self.chatText.insert(Tkinter.END,'聊天服务器工作端口：')
        self.chatText.insert(Tkinter.END,self.port)
        
        while True:
            # Get the list sockets which are ready to be read through select
            self.read_sockets,self.write_sockets,self.error_sockets = select.select(self.CONNECTION_LIST,[],[])
            for self.sock in self.read_sockets:
                if len(self.CONNECTION_LIST)>(maxpeople+1):
                    self.chatText.insert(Tkinter.END, " 人数超过限制！")
                    self.broadcast_data(self.sock, "用户已下线: (%s, %s)" % self.addr)
                    print "用户 (%s, %s) 下线了" % self.addr
                    self.sock.close()
                    self.CONNECTION_LIST.remove(self.sock)
                # new connection
                if self.sock==self.serverSock:
                    self.sockfd,self.addr=self.serverSock.accept()
                    self.CONNECTION_LIST.append(self.sockfd)
                    print "用户 (%s, %s) 已连接" % self.addr
                    a=("用户已连接",self.addr)
                    self.broadcast_data(self.sockfd, "新用户!: [%s:%s]\n" % self.addr)
                    self.chatText.insert(Tkinter.END,a)
                
                # Some incoming message from a client
                else:
                    try:
                            self.clientMsg = self.sock.recv(self.buffer)
                            if self.clientMsg :
                                theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                self.broadcast_data(self.sock, "\r" + '<' + str(self.sock.getpeername()) + '> ' +theTime+'说：\t' +self.clientMsg) 
                                self.chatText.insert(Tkinter.END, '<' + str(self.sock.getpeername()) + '>'  + theTime +' 说：\n')
                                self.chatText.insert(Tkinter.END, '  ' +self.clientMsg)
                            
                    except:
                            m=("用户已下线:\t",self.addr)
                            self.chatText.insert(Tkinter.END, m)
                            self.broadcast_data(self.sock, "用户已下线: (%s, %s)" % self.addr)
                            print "用户 (%s, %s)下线了" % self.addr
                            self.sock.close()
                            self.CONNECTION_LIST.remove(self.sock)
                            continue
                    
        self.serverSock.close()
    def close(self):  
        sys.exit()  
      
     
    def startNewThread(self):  
        '''
        启动一个新线程来接收客户端的消息  
        thread.start_new_thread(function,args[,kwargs])函数原型，  
        其中function参数是将要调用的线程函数，args是传递给线程函数的参数，它必须是个元组类型，而kwargs是可选的参数  
        receiveMessage函数不需要参数，就传一个空元组
        '''
        thread.start_new_thread(self.receiveMessage,())  
    def broadcast_data (self,sock, message):
        for socket in self.CONNECTION_LIST:
            if socket != self.serverSock and socket != sock :
                try :
                    socket.send(message)
                except :
                    # chat client pressed ctrl+c 
                    socket.close()
                    self.CONNECTION_LIST.remove(socket)
                
def main():
    global   maxpeople
    maxpeople=input("最多几人对话？请输入相应数字\n")
    server = ServerUI()  
    server.startNewThread()  
    server.root.mainloop()  
      
if __name__=='__main__':
    reload(sys)  
    sys.setdefaultencoding('utf8')
    main()  
