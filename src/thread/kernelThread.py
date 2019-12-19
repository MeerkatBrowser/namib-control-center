import subprocess
import notification
from PyQt5.QtCore import QThread, pyqtSignal

class kernelThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        kernel = []
        stableBtn = ""
        ltsBtn = ""
        hardBtn = ""
        zenBtn = ""

        try:
            stableVersion = (
                subprocess.check_output(
                    ["pacman -Qi linux | grep 'Version'"],
                    stderr=subprocess.STDOUT,
                    shell=True,
                )
                .decode("ascii")
                .replace("Version         : ", "")
            )
        except subprocess.CalledProcessError:
            stableVersion = "Kernel not installed !"

        try:
            ltsVersion = (
                subprocess.check_output(
                    ["pacman -Qi linux-lts | grep 'Version'"],
                    stderr=subprocess.STDOUT,
                    shell=True,
                )
                .decode("ascii")
                .replace("Version         : ", "")
            )
        except subprocess.CalledProcessError:
            ltsVersion = "Kernel not installed !"

        try:    
            hardVersion = (
                subprocess.check_output(
                    ["pacman -Qi linux-hardened | grep 'Version'"],
                    stderr=subprocess.STDOUT,
                    shell=True,
                )
                .decode("ascii")
                .replace("Version         : ", "")
            )
        except subprocess.CalledProcessError:
            hardVersion = "Kernel not installed !"

        try:
            zenVersion = (
                subprocess.check_output(
                    ["pacman -Qi linux-zen | grep 'Version'"],
                    stderr=subprocess.STDOUT,
                    shell=True,
                )
                .decode("ascii")
                .replace("Version         : ", "")
            )
        except subprocess.CalledProcessError:
            zenVersion = "Kernel not installed !"

            try:
                remoteStable = (
                    subprocess.check_output(
                        ["pacman -Si linux | grep 'Version'"],
                        stderr=subprocess.STDOUT,
                        shell=True,
                    )
                    .decode("ascii")
                    .replace("Version         : ", "")
                )
                remoteLts = (
                    subprocess.check_output(
                        ["pacman -Si linux-lts | grep 'Version'"],
                        stderr=subprocess.STDOUT,
                        shell=True,
                    )
                    .decode("ascii")
                    .replace("Version         : ", "")
                )
                remoteHard = (
                    subprocess.check_output(
                        ["pacman -Si linux-hardened | grep 'Version'"],
                        stderr=subprocess.STDOUT,
                        shell=True,
                    )
                    .decode("ascii")
                    .replace("Version         : ", "")
                )
                remoteZen = (
                    subprocess.check_output(
                        ["pacman -Si linux-zen | grep 'Version'"],
                        stderr=subprocess.STDOUT,
                        shell=True,
                    )
                    .decode("ascii")
                    .replace("Version         : ", "")
                )
            except subprocess.CalledProcessError:
                notification.notify("Error getting kernels version !")

        if (
            stableVersion != remoteStable
            and stableVersion != "Kernel not installed !"
            or ltsVersion != remoteLts
            and ltsVersion!= "Kernel not installed !"
            or hardVersion != remoteHard
            and hardVersion != "Kernel not installed !"
            or zenVersion != remoteZen
            and zenVersion != "Kernel not installed !"
        ):
            notification.notify("A kernel update is available !")
        
        if (stableVersion == remoteStable):
            stableBtn = "Uninstall kernel !"
        elif (stableVersion != remoteStable):
            stableBtn = "Install/Update kernel !"
    
        if (ltsVersion == remoteLts):
            ltsBtn = "Uninstall kernel !"
        elif (ltsVersion != remoteLts):
            ltsBtn = "Install/Update kernel !"
    
        if (hardVersion == remoteHard):
            hardBtn = "Uninstall kernel !"
        elif (hardVersion != remoteHard):
            hardBtn = "Install/Update kernel !"
    
        if (zenVersion == remoteZen):
            zenBtn = "Uninstall kernel !"
        elif (zenVersion != remoteZen):
            zenBtn = "Install/Update kernel !"

        kernel.extend([stableVersion, ltsVersion, hardVersion, zenVersion, remoteStable, remoteLts, remoteHard, remoteZen, stableBtn, ltsBtn, hardBtn, zenBtn])
            
        self.signal.emit(kernel)