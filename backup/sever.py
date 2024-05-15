#2024-5-15 22:38
import threading
import game
import socket
import json

class User:
    def __init__(self,client):
        self.username=''
        self.password=''
        self.confirm_password=''
        self.client=client

    def register(self):
        self.client.send('请输入用户名: '.encode('utf-8'))
        self.username = self.client.recv(1024).decode('utf-8')
        while True:
            if self.username in users:
                self.client.send('用户名已存在，请重新输入！'.encode('utf-8'))
                self.client.send('请输入用户名: '.encode('utf-8'))
                self.username = self.client.recv(1024).decode('utf-8')
                continue  # 跳过密码输入的部分，直接回到用户名输入
            while True:
                self.client.send('请输入密码:'.encode('utf-8'))
                self.password = self.client.recv(1024).decode('utf-8')
                self.client.send('请再次输入密码以确认:'.encode('utf-8'))
                self.confirm_password = self.client.recv(1024).decode('utf-8')
                if self.password == self.confirm_password:
                    users[self.username] = self.password
                    self.client.send('注册成功！'.encode('utf-8'))
                    break  # 如果两次密码一致，则跳出循环
                else:
                    self.client.send('两次输入的密码不一致，请重新输入密码！'.encode('utf-8'))
            break

        with open('user_info.txt', 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)

    def login(self):
        self.client.send('请输入用户名:'.encode('utf-8'))
        self.username = self.client.recv(1024).decode('utf-8')
        if self.username not in users:
            self.client.send('用户名不存在，请先注册！'.encode('utf-8'))
            return
        while True:
            self.client.send('请输入密码:'.encode('utf-8'))
            self.password = self.client.recv(1024).decode('utf-8')
            if self.password == users[self.username]:
                self.client.send('登录成功！'.encode('utf-8'))
                break
            else:
                self.client.send('密码错误，请重新输入！'.encode('utf-8'))

class Server:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.clients = []

    def receive(self):
        print('wating for conection...')
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")
            #self.clients.append(client)
            new_user=User(client)
            message = client.recv(1024).decode('utf-8')
            while True:
                choice = message
                if choice == "1":
                    new_user.register()
                    break
                elif choice == "2":
                    new_user.login()
                    break
                elif choice == "3":
                    client.send('程序退出！'.encode('utf-8'))
                    break
                else:
                    client.send('无效的选择，请重新输入！'.encode('utf-8'))
            thread = threading.Thread(target=self.handle, args=(client,))
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

    sever=Server()
    server_thread = threading.Thread(target=sever.run)
    server_thread.start()






