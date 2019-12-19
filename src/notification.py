import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify



def notify(i):
    Notify.init("Namib Controler Center")
    notification = Notify.Notification.new(i).show()
