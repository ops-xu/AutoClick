import sys
from pathlib import Path
from PyInstaller import __main__ as pyi

# 应用程序的入口文件
entry_file = Path("main.py")

# 打包选项
options = [
    "--name=TimerClick",
    "--onefile",
    "--noconsole",
    "--hidden-import=tkinter",
    "--hidden-import=keyboard",
    "--hidden-import=pyautogui",
    "--hidden-import=time",
    "--hidden-import=threading",
    "--hidden-import=datetime",
]

# 执行打包
args = ["pyinstaller", *options, str(entry_file)]
sys.argv[1:] = args
pyi.run()
