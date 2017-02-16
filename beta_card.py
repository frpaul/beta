#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''Show cards with greek words from base'''

import pygtk
pygtk.require('2.0')
import gtk
import codecs
import re
import os
import sys

import random

import sqlite3

def destroy_cb(widget):
    gtk.main_quit()
    return False

class Engine:
    def __init__(self):

        conn = self.open_base()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) AS RowNum FROM dictionary")

        self.r_num = cur.fetchone()[0]

        cur.close()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Learn greek")
        self.window.set_border_width(10)
        self.window.set_size_request(250, 100)
        self.window.connect("destroy", destroy_cb) 
        self.window.connect("key-press-event", self.manager_keys) 

        self.vbox = gtk.VBox(False, 0)

        self.label = gtk.Label()

        self.vbox.pack_start(self.label, False, False, 1)

        self.window.add(self.vbox)
        self.label.show()
        self.vbox.show()
        self.window.show()

        self.cur_row = self.get_row()
        # show next random greek word from base
        self.label.set_text(self.cur_row[1])

    def open_base(self):
        # should check if the base is already opened

        conn = sqlite3.connect('beta_dict')

        return conn

    def get_row(self):

        ran = random.randint(0, self.r_num)
        conn = self.open_base()
        cur = conn.cursor()

        command = "SELECT * FROM dictionary WHERE a_num=:r"

        cur.execute(command, {"r": ran})
        res = cur.fetchall()[0]

        cur.close()

        return res

    def manager_keys(self, widget, event):        
        """Callback for input widget"""

        keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & gtk.gdk.CONTROL_MASK:

            if keyname == "n":
                self.cur_row = self.get_row()
                # show next random greek word from base
                self.label.set_text(self.cur_row[1])
            if keyname == "h":
                self.label.set_text(self.cur_row[2])


######################3
def main():
    gtk.main()
    return 0


eng = Engine()
#print eng.get_rand(15)
#print eng.get_row()

main()
