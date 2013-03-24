"""
Really simple desktop notifications
"""
import hashlib
import os

import dbus

DEFAULT_DURATION = 0

def show(app, icon, title, message, duration=DEFAULT_DURATION):
    bus = dbus.SessionBus()
    proxy = bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
    notid = dbus.Interface(proxy, "org.freedesktop.Notifications")

    notificationId = str(int(hashlib.md5('%s-%s' % (title, message)).hexdigest(), 16))[-5:]

    # if os.path.exists(icon):
    #     icon = 'file://%s' % icon

    notid.Notify(app, int(notificationId), icon, title, message, [], {}, duration)
