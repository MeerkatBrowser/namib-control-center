import subprocess
import notification
from PyQt5.QtCore import QThread, pyqtSignal

class commandThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.cmd = ""

    def run(self):
        process = subprocess.Popen(
            self.cmd, shell=True, stdin=subprocess.PIPE , stdout=subprocess.PIPE, universal_newlines=True
        )
        logging = ""
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                logging += "Process completed !"
                notification.notify("Process completed !")
                self.signal.emit(logging)
                break
            if output:
                logging += output
                self.signal.emit(logging)