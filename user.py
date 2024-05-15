
users = {}

def register():
    username = input("请输入用户名: ")
    while True:
        if username in users:
            print("用户名已存在，请重新输入！")
            username = input("请输入用户名: ")
            continue  # 跳过密码输入的部分，直接回到用户名输入
        while True:
            password = input("请输入密码: ")
            confirm_password = input("请再次输入密码以确认: ")
            if password == confirm_password:
                users[username] = password
                print("注册成功！")
                break  # 如果两次密码一致，则跳出循环
            else:
                print("两次输入的密码不一致，请重新输入密码！")
        break

def login():
    username = input("请输入用户名: ")
    if username not in users:
        print("用户名不存在，请先注册！")
        return
    while True:
        password = input("请输入密码: ")
        if password == users[username]:
            print("登录成功！")
            break
        else:
            print("密码错误，请重新输入！")



'''while True:
    print("""  
    1. 注册  
    2. 登录  
    3. 退出  
    """)
    choice = input("请选择操作（输入编号）: ")
    if choice == "1":
        register()
    elif choice == "2":
        login()
        break
    elif choice == "3":
        print("程序退出。")
        break
    else:
        print("无效的选择，请重新输入！")'''