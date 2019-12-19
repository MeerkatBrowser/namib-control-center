#!/usr/bin/python3

import sys
import subprocess
from PyQt5 import QtWidgets

from mainWindow import Ui_MainWindow
from thread import commandThread, kernelThread

class nccApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(nccApp, self).__init__(parent)
        self.setupUi(self)
        self.exitLog.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))

        self.command_thread = commandThread.commandThread()
        self.command_thread.signal.connect(self.command_result)

        self.kernel_thread = kernelThread.kernelThread()
        self.kernel_thread.signal.connect(self.kernel_result)
        self.kernel_thread.start()

        self.stableKernelBtn.clicked.connect(self.stableKernelCommand)
        self.ltsKernelBtn.clicked.connect(self.ltsKernelCommand)
        self.hardenedKernelBtn.clicked.connect(self.hardenedKernelCommand)
        self.zenKernelBtn.clicked.connect(self.zenKernelCommand)

    def start_command(self, cmd):
        self.stackedWidget.setCurrentIndex(1)
        self.exitLog.setEnabled(False)
        self.command_thread.cmd = cmd
        self.command_thread.start()

    def command_result(self, result):
        self.scrollbar = self.logText.verticalScrollBar()
        if "Process completed !" in result:
            self.exitLog.setEnabled(True)
            self.logText.setText(result)
            self.scrollbar.setValue(self.scrollbar.maximum())
            self.kernel_thread.start()
        else:
            self.logText.setText(result)
            self.scrollbar.setValue(self.scrollbar.maximum())

    def kernel_result(self, result):
        self.stableKernelSystemLabel.setText("Local : " + result[0])
        self.stableKernelRepositoryLabel.setText("Remote : " + result[4])
        self.stableKernelBtn.setText(result[8])
        self.ltsKernelSystemLabel.setText("Local : " + result[1])
        self.ltsKernelRepositoryLabel.setText("Remote : " + result[5])
        self.ltsKernelBtn.setText(result[9])
        self.hardenedKernelSystemLabel.setText("Local : " + result[2])
        self.hardenedKernelRepositoryLabel.setText("Remote : " + result[6])
        self.hardenedKernelBtn.setText(result[10])
        self.zenKernelSystemLabel.setText("Local : " + result[3])
        self.zenKernelRepositoryLabel.setText("Remote : " + result[7])
        self.zenKernelBtn.setText(result[11])

    def stableKernelCommand(self):
        if self.stableKernelBtn.text() == "Uninstall kernel !":
            self.start_command(
                "pkexec pacman --noconfirm -Rs linux linux-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )
        elif self.stableKernelBtn.text() == "Install/Update kernel !":
            self.start_command(
                "pkexec pacman --noconfirm -Syy linux linux-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )
        
    def ltsKernelCommand(self):
        if self.ltsKernelBtn.text() == "Uninstall kernel !":
            self.start_command(
                "pkexec pacman --noconfirm -Rs linux-lts linux-lts-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )
        elif self.ltsKernelBtn.text() == "Install/Update kernel !":
            self.start_command(
                "pkexec pacman --noconfirm -Syy linux-lts linux-lts-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )

    def hardenedKernelCommand(self):
        if self.hardenedKernelBtn.text() == "Uninstall kernel !":
            self.start_command(
                "pkexec pacman --noconfirm -Rs linux-hardened linux-hardened-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )
        elif self.hardenedKernelBtn.text() == "Install/Update kernel !":
            self.start_command(
                "pkexec pacman -Syy --noconfirm linux-hardened linux-hardened-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )

    def zenKernelCommand(self):
        if self.zenKernelBtn.text() == "Uninstall kernel !":
            self.start_command(
                "pkexec pacman --noconfirm -Rs linux-zen linux-zen-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )
        elif self.zenKernelBtn.text() == "Install/Update kernel !":
            self.start_command(
                "pkexec pacman --noconfirm -Syy linux-zen linux-zen-headers && pkexec grub-mkconfig -o /boot/grub/grub.cfg"
            )
            


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = nccApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
