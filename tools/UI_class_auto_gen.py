from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtCore import QCoreApplication, QObject
import sys
import os
from os import listdir
from os.path import isfile, join
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

app=QCoreApplication(sys.argv)
def directory_changed(path):
    print('Directory Changed!!!')

def file_changed(path):
    # pyuic6 -x .\ui\actor_info.ui -o ui_elements/actor_info.py
    file_name=os.path.splitext(os.path.basename(path))
    n=rf"C:\Users\pc\Documents\programming\personal_projects\invoice_creator\ui_elements\ui_templates\{file_name[0]}.py"
    command=f"pyuic6 -x {path} -o {n}"
    print(f"generating {file_name[0]}")
    os.system(command)



obj=QObject(app)
watcher = QFileSystemWatcher(obj)
path=r"C:\Users\pc\Documents\programming\personal_projects\invoice_creator\ui"
for file in [f for f in listdir(path) if isfile(join(path, f))]:
    print(f"watching {file}")
    watcher.addPath(rf"{path}\{file}")
watcher.fileChanged.connect(file_changed)

app.exec()

