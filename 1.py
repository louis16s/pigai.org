import time
import os
from configparser import ConfigParser
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from playwright.sync_api import Playwright, sync_playwright, expect


version_info = '1.0'
filename = 'essay.txt'

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False)
    context = browser.new_context()
    page = context.new_page()
    #page.route("**/*.jpg", lambda route: route.abort())
    page.goto("http://www.pigai.org/")
    page.get_by_placeholder("手机号|邮箱|用户名").fill(user)
    page.get_by_placeholder("密码").fill(password)
    page.locator("#ulogin").get_by_role("img").click()
    page.get_by_role("textbox").fill(essay_id)#"2831395"
    page.get_by_role("textbox").press("Enter")
    page.locator("#contents").click()
    page.locator("#contents").fill(essay)
    #page.get_by_role("link", name="保存数据").click()

    for i in range(9):
        time.sleep(9999)
    # ---------------------
    context.close()
    browser.close()

def read_file(name):
    file = open(name, 'r')
    essay = file.read()
    file.close()
    return essay

def pwd_input():  # 密码
    import msvcrt
    chars = []
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
        if newChar in '\r\n':  # 如果是换行，则输入结束
            break
        elif newChar == '\b':  # 如果是退格，则删除密码末尾一位并且删除一个星号
            if chars:
                del chars[-1]
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格
                msvcrt.putch(' '.encode(encoding='utf-8'))  # 输出一个空格覆盖原来的星号
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格准备接受新的输入
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8'))  # 显示为星号
    return (''.join(chars))

def printer(content,style0):  # 彩色输出
    console = Console()
    console.print(content, style=style0)

def file1():  # 文件读写
    import cryptocode
    import win32con, win32api
    global user, password, local
    console = Console()
    file = open(filename, 'a+')
    file.close()
    if os.path.exists('account.ini'):  # 文件存在检测
        # printer('file existed','yellow')
        cf = ConfigParser()
        cf.read('account.ini')
        version = cf.get('parm', 'ver')
        if version < version_info:
            os.remove('account.ini')
            with console.screen(style="bold white on red") as screen:
                text = Align.center("[blink]配置文件\n版本过低\n自动删除[/blink]", vertical="middle")
                screen.update(Panel(text))
                time.sleep(5)
            file1()
        # main
        user = cf.get('main', 'uid')
        password = cf.get('main', 'pwd')
        # parm
        local = cf.get('parm', 'local')


    else:
        printer('config file not fund','yellow')
        os.system('mode con cols=30 lines=9')
        printer("批改网专用-可以粘贴器",'yellow')
        printer('密码会自动加密','yellow')
        printer('input account','yellow')
        user = input()
        printer('input password','yellow')
        password = pwd_input()
        print(' ')
        printer('浏览器选择','yellow')
        printer('edge(1)|chrome(2)','yellow')
        local = input()
        t0 = '\n'
        password = cryptocode.encrypt(password, 'louis16s')  # 加密

        with open('account.ini', "w") as file:
            file.write(
                '[main]' + t0 +
                'uid = ' + str(user) + t0 +
                'pwd = ' + str(password) + t0 +
                '[parm]' + t0 +
                'local = ' + str(local) + t0 +
                'ver = ' + version_info + t0)
            file.close()

        for step in track(range(100), description="Writing..."):
            time.sleep(0.01)
        printer('config is generated','yellow')
        win32api.SetFileAttributes('account.ini', win32con.FILE_ATTRIBUTE_HIDDEN)

    password = cryptocode.decrypt(password, 'louis16s')  # 解密
    # 浏览器
    if local == '0':
        local = None  # Chromium
    if local == '1':
        local = 'msedge'
    if local == '2':
        local = 'chrome'

    return user, password, local

if __name__ == '__main__':
    file1()
    os.system('mode con cols=40 lines=8')
    printer('version ' + version_info + ' by louis16s','yellow')
    printer("批改网专用-可以粘贴器",'blue')
    printer("内容请先放入同一文件夹下的"+filename+"中",'green')
    printer('再输入作文号','red')
    essay_id = str(input("作文号："))
    essay = read_file(filename)
    with sync_playwright() as playwright:
        run(playwright)