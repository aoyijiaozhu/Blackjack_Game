import threading
import game
import socket
import json


class User:
    def __init__(self,client):
        self.username=''
        self.password=''
        self.confirm_password=''

    def register(self,client):  #注册
        client.send('请输入用户名: '.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        while True:
            if username in users:
                client.send('用户名已存在，请重新输入！'.encode('utf-8'))
                client.send('请输入用户名: '.encode('utf-8'))
                username = client.recv(1024).decode('utf-8')
                continue  # 跳过密码输入的部分，直接回到用户名输入
            while True:
                client.send('请输入密码:'.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')
                client.send('请再次输入密码以确认:'.encode('utf-8'))
                confirm_password = client.recv(1024).decode('utf-8')
                if password == confirm_password:
                    users[username] = password
                    client.send('注册成功！'.encode('utf-8'))
                    break  # 如果两次密码一致，则跳出循环
                else:
                    client.send('两次输入的密码不一致，请重新输入密码！'.encode('utf-8'))
            break

        with open('user_info.txt', 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
        return username

    def login(self,new_user,client):    #登录
        client.send('请输入用户名:'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        while True:
            if username not in users:
                client.send('用户名不存在，请先注册！'.encode('utf-8'))
                new_user.register(self.client)
                break
            while True:
                client.send('请输入密码:'.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')
                if password == users[username]:
                    client.send('登录成功！'.encode('utf-8'))
                    break
                else:
                    client.send('密码错误，请重新输入！'.encode('utf-8'))
            break
        return username

class Server:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []
        self.usernames = []
        self.lock = threading.Lock()  # 线程锁

    def broadcast(self, message):   #广播消息
        for client in self.clients:
            client.send(message)

    def handle(self,client):    #处理消息
        while True:
            try:
                index = self.clients.index(client)
                username = self.usernames[index]
                print(index)
                print(username+'123123123131231231231')
                message = client.recv(1024).decode('utf-8')
                message=f"<{username},{message}>".encode('utf-8')   #定义广播格式
                print(message)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                username = self.usernames[index]
                client.close()
                self.usernames.remove(username)
                print(f'{username} 离开了游戏')
                self.broadcast(f'{username} 离开了游戏!'.encode('utf-8'))
                print(self.usernames)
                break

    def login_sign(self, client):  # 处理注册和登录的过程
        new_user=User(client)
        message = client.recv(1024).decode('utf-8')
        while True:
            choice = message
            if choice == "1":
                self.lock.acquire()  # 获取锁
                self.usernames.append(new_user.register(client))
                self.lock.release()  # 释放锁
                print(self.usernames)
                break
            elif choice == "2":
                self.lock.acquire()  # 获取锁
                self.usernames.append(new_user.login(new_user,client))
                self.lock.release()  # 释放锁
                print(self.usernames)
                break
            elif choice == "3":
                client.send('程序退出！'.encode('utf-8'))
                return
            else:   #实际上这个用不上
                client.send('无效的选择，请重新输入！'.encode('utf-8'))
                break
        thread = threading.Thread(target=self.handle, args=(client,))
        thread.start()

    def receive(self):      #接收客户端连接
        print('wating for conection...')
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")
            self.clients.append(client)
            thread = threading.Thread(target=self.login_sign, args=(client,))  # 创建新的线程来处理注册和登录的过程
            thread.start()

    def run(self):
        print("Server started...")
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

if __name__ == '__main__':
    game=game.Game()
    game.startGame()

    with open('user_info.txt', 'r', encoding='utf-8') as file:
        user_info_str = file.read()
    users = json.loads(user_info_str)

    print(users)

    server=Server()
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
