import socket
import threading


class Client:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def write(self):
        while True:
            print("""  
                    1. 注册  
                    2. 登录  
                    3. 退出  
                    """)
            choice = input("请选择操作（输入编号）: ")
            self.client.send(choice.encode('utf-8'))
            if choice == "1" or choice == "2" or choice == "3":
                break
        while True:
            self.client.send(input('').encode('utf-8'))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                print(message)
            except:
                print("An error occured!")
                self.client.close()
                break

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == '__main__':
    client=Client()
    client2_thread = threading.Thread(target=client.run)
    client2_thread.start()


    '''if choice == "1":
            user.register()
        elif choice == "2":
            user.login()
            break
        elif choice == "3":
            print("程序退出。")
            break
        else:
            print("无效的选择，请重新输入！")'''
