#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import

import re
import gi
import signal
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import AppIndicator3 as appindicator
from .common import *
from .database import DictTable, SentenceTable


def main():
    indicator = appindicator.Indicator.new_with_path(APPINDICATOR_ID,
                                                     APPINDICATOR_ICON,
                                                     appindicator.IndicatorCategory.SYSTEM_SERVICES,
                                                     ICON_THEM_PATH)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()


def build_menu():
    menu = gtk.Menu()

    item_show = gtk.MenuItem('Save It')
    item_show.connect('activate', DictAction.save)
    menu.append(item_show)

    item_web = gtk.MenuItem('Open Web')
    item_web.connect('activate', DictAction.web)
    menu.append(item_web)

    item_server = gtk.MenuItem('Server')
    menu.append(item_server)

    submenu = gtk.Menu()
    item_server.set_submenu(submenu)

    item_stop = gtk.MenuItem('Stop')
    item_stop.connect('activate', DictAction.stop)
    submenu.append(item_stop)

    item_start = gtk.MenuItem('Start')
    item_start.connect('activate', DictAction.start)
    submenu.append(item_start)

    item_reload = gtk.MenuItem('Reload')
    item_reload.connect('activate', DictAction.reload)
    submenu.append(item_reload)

    item_about = gtk.MenuItem('About')
    item_about.connect('activate', DictAction.about)
    menu.append(item_about)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', DictAction.quit)
    menu.append(item_quit)

    menu.show_all()
    return menu


class AboutWindow(gtk.Window):
    """
    docstring for AboutWindow
    """
    def __init__(self):
        gtk.Window.__init__(self, title="About Dict Hub")
        self.set_default_size(400, 200)

        cbox = gtk.Box(spacing=10)
        cbox.set_homogeneous(False)
        inbox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=10)
        inbox.set_homogeneous(False)

        cbox.pack_start(inbox, True, True, 0)

        label = gtk.Label()
        label.set_markup('')
        inbox.pack_start(label, True, True, 0)

        label = gtk.Label()
        label.set_markup('<b><big>DictHub %s</big></b>' % APP_VERSION)
        inbox.pack_start(label, True, True, 0)

        tlist = ('',
                 'A Simple Tool For Store Dict And Stencence',
                 'Copyright @ 2017-2020 Hanson Leungh',
                 '')
        for t in tlist:
            label = gtk.Label(t)
            inbox.pack_start(label, True, True, 0)

        label = gtk.Label()
        label.set_markup('<a href="https://github.com/liangguohuan/DictHub">'
                         'https://github.com/liangguohuan/DictHub</a>'
                         '\n')
        inbox.pack_start(label, True, True, 0)

        self.add(cbox)


class DictAction:
    """
    docstring for DictAction
    """
    @classmethod
    def save(cls, _):
        cb = gtk.Clipboard.get(gdk.SELECTION_PRIMARY)
        text = cb.wait_for_text()

        if len(text.split(' ')) > 1:
            tbl = SentenceTable()
            text = re.sub(r'(\s+)|(\n)', ' ', text)
            text = text.strip()
            text = text.capitalize()
            fields = {'sentence': text}
        else:
            tbl = DictTable()
            text = re.sub(r'(^[^A-Za-z]+)|([^A-Za-z]+$)', '', text)
            text = text.lower()
            fields = {'name': text}

        if text != '':
            tbl.insert(fields)

    @classmethod
    def stop(cls, _):
        shell_exec('systemctl stop dict-web.service')

    @classmethod
    def start(cls, _):
        shell_exec('systemctl start dict-web.service')

    @classmethod
    def reload(cls, _):
        shell_exec('systemctl reload dict-web.service')

    @classmethod
    def web(cls, _):
        wrapper = 'start-stop-daemon --start --background --name=docweb --exec'
        openstr = '/usr/bin/xdg-open http://localhost:%d' % WEB_PORT_DEFAULT
        cmd = '%s %s' % (wrapper, openstr)
        shell_exec(cmd)

    @classmethod
    def about(cls, _):
        window = AboutWindow()
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.main()

    @classmethod
    def quit(cls, _):
        gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
