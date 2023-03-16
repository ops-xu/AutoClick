import datetime
import threading
import time
from tkinter import *
import pyautogui
import keyboard


class ClickThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            pyautogui.leftClick()
            time.sleep(0.02)

    def stop(self):
        self._stop_event.set()


class AutoClicker(threading.Thread):
    def __init__(self):
        self.clicking = False
        self.ch = None

    def start_clicking(self):
        if not self.clicking:
            self.ch = ClickThread()
            self.ch.daemon = True
            self.ch.start()
            self.clicking = True

    def stop_clicking(self):
        self.clicking = False
        self.ch.stop()
        self.ch.join()


clicker = AutoClicker()


class TimeThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            now = datetime.datetime.now()
            dstr.set(now.strftime('%H:%M:%S'))
            count_time = str(timeInp.get()).strip()
            interval = int(intervalInp.get().strip())
            if len(count_time) == 19:
                end = datetime.datetime.strptime(count_time, '%Y-%m-%d %H:%M:%S')
                count_down = round((end - now).total_seconds() * 1000)
                count_dstr.set('{:,}'.format(count_down))
                if count_down <= interval:
                    clicker.start_clicking()
                    break
            time.sleep(0.02)

    def stop(self):
        self._stop_event.set()


class AutoTimer(threading.Thread):
    def __init__(self):
        self.starting = False
        self.th = None

    def start(self):
        if not self.starting:
            self.th = TimeThread()
            self.th.daemon = True
            self.th.start()
            self.starting = True

    def stop(self):
        self.starting = False
        self.th.stop()
        self.th.join()


timer = AutoTimer()


def on_hotkeyf8():
    timer.start()


def on_hotkeyf7():
    try:
        timer.stop()
        clicker.stop_clicking()
    except:
        print('error')


keyboard.add_hotkey('f8', on_hotkeyf8)
keyboard.add_hotkey('f7', on_hotkeyf7)

if __name__ == '__main__':
    root = Tk()
    # 设置窗口处于顶层
    root.attributes('-topmost', True)
    root.wm_title("定时自动点击器")
    # 设置窗口大小变量
    width = 600
    height = 300
    # 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size_geo)

    dstr = StringVar()
    Label(root, textvariable=dstr, fg='green', font=("微软雅黑", 85)).pack(side='bottom')

    count_dstr = StringVar()
    count_dstr.set("倒计时：0")
    count = Label(root, textvariable=count_dstr, bg="yellow", font=("微软雅黑", 20))
    count.pack(side='top')

    # 添加文本内,设置字体的前景色和背景色，和字体类型、大小
    lab = Label(root, text="F8开启 F7停止", bg="yellow", fg="red", font=('Times', 20, 'bold italic'))
    # 将文本内容放置在主窗口内
    lab.pack()

    timeLab = Label(root, text="定时时间格式：2023-03-12 20:05:00", font=("微软雅黑", 11), fg="gray")
    timeLab.place(relx=0.05, y=60, height=30)
    timeInp = Entry(root, font=("微软雅黑", 10))
    timeInp.place(relx=0.05, y=90, height=30)
    today = datetime.datetime.now().date()
    eight_pm = datetime.time(hour=21, minute=0)
    today_eight_pm = datetime.datetime.combine(today, eight_pm)
    timeInp.insert(0, str(today_eight_pm))

    intervalLab = Label(root, text="误差范围毫秒，0代表准时准点，1000代表提前1秒连点，100代表提前100毫秒连点",
                        font=("微软雅黑", 11), fg="gray")
    intervalLab.place(relx=0.05, y=120, height=30)
    intervalInp = Entry(root, font=("微软雅黑", 10))
    intervalInp.place(relx=0.05, y=150, height=30)
    intervalInp.insert(0, "0")

    root.mainloop()
