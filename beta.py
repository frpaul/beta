#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''Набивалка для моей базы древнегреческих слов'''

import pygtk
pygtk.require('2.0')
import gtk
import codecs
import re
import os
import sys

import logging
import ConfigParser
import unicodedata
import sqlite3

import hipconv
import russ_simp
from betacode import Beta

beta = Beta()
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", filename="beta_tools.log", filemode="w", level=logging.INFO)

conv = hipconv.Repl()

russ = russ_simp.Mn(True, True, True)

def destroy_cb(widget):
    gtk.main_quit()
    return False

class Engine():
    """Main engine. Base handler"""

    def __init__(self, base_name=None, table_name=None):
        # crappy regex, have to fix
        self.reg = re.compile('^(.+?) (?:slav) (.+?) (?:desc) (.+?)$', re.U)
        self.cols = ["b_greek", "c_slav", "d_rus", "e_desc"]
#        self.b_name = b_name

        ###### Configuration ###########

        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.join(os.path.expanduser('~'), '.config', 'hiptools', 'betarc'))

        if base_name:
            self.b_name = base_name
        else:
            self.b_name = self.config.get('Paths', 'beta_path')

        if table_name:
            self.table_name = table_name
        else:
            self.table_name = self.config.get('Tables', 'beta_tab')

        self.sl_conv = True # славянскую колонку - в юникод. TODO: Если хотим править в hip - False

        combo_tmp = self.config.get('SearchOptions', 'default_search')

        cmb_ls = ['Greek', 'Betacode', 'Slavonic']
        for s in range(len(cmb_ls)):
            if combo_tmp == cmb_ls[s]:
                self.cmb_active = s # 0, 1 or 2 - for ComboBox
                self.search_col_sw = s # 0, 1, 2 - for my search engine. Stupid, aye?
        self.gr_font = self.config.get('Fonts', 'gr_font')
        self.sl_font = self.config.get('Fonts', 'sl_font')
        #################################


    def toggler (self, widget):
        ''' callback for combobox 
        '''
        # greek, betacode, slavic column

        name = widget.get_active_text() 
        if name == 'Greek':
            self.search_col_sw = 0
        elif name == 'Betacode':
            self.search_col_sw = 1
        elif name == 'Slavonic':
            self.search_col_sw = 2

    def sl_edited_cb(self, cellr, entry, path, num):

        iter1 = self.model.get_iter(path)
        hip_ln = self.model.get_value(iter1, 9)
        
        entry.set_text(hip_ln)

    def edited_cb(self, cell, path, new_text, num):
        """Save changes in GUI (tree-view) to tree-model."""

        iter1 = self.model.get_iter(path)
        if num == 2:
            new_text = conv(new_text, 'uni')
        self.model.set_value(iter1, num, new_text)          

        key = self.model.get_value(iter1, 0)

        command = "UPDATE " + self.table_name + " SET " + self.cols[num - 1] + "=\"" + new_text + "\" WHERE a_num=\"" + str(key) + "\""
        
        self.edit_base(command)

    def ins_tree(self):
        """Get data from base, insert into TreeModel"""

        command = "SELECT * FROM " + self.table_name + " ORDER BY greek"

#       common: a_num, b_greek, c_slav, d_rus, e_desc, greek, beta, slav, source

        rows = self.get_f_base(command)
#        print rows
        for row in rows:
            iter = self.model.append()

            hip_ln = row[2]

            if self.sl_conv:
                conv_txt = conv(hip_ln, 'uni')
            else:
                conv_txt = hip_ln

#            rus_txt = russ.conv_str(hip_ln)

            self.model.set(iter, 0, row[0])     # a_num
            self.model.set(iter, 1, row[1])     # b_greek 
            self.model.set(iter, 2, conv_txt)   # slavic, converted to unicode
            self.model.set(iter, 3, row[3])     # russian
            self.model.set(iter, 4, row[4])     # description (should convert to unicode)
            self.model.set(iter, 5, row[5])     # greek (без надстрочников) - для поиска
            self.model.set(iter, 6, row[6])     # beta (betacode) - для поиска
            self.model.set(iter, 7, row[7])    # slavic (в русской транскрипции) - для поиска
            self.model.set(iter, 8, row[8])    # source (книжка, откуда взяли примеры)
            self.model.set(iter, 9, hip_ln)     # hip for slavic  (2)

        self.selection.select_path((0,))

    def on_key_press_event(self, widget, event):
        """Callback for editor (TreeView)"""

        keyname = gtk.gdk.keyval_name(event.keyval)

        global res_num
        selection = self.selection
        model, path = selection.get_selected_rows()

        if isinstance(widget, gtk.TreeView):

            if event.state & gtk.gdk.CONTROL_MASK:
                if keyname == "d":
                    
                    iter2 = model.get_iter(path[0])
                    print 'deleting', model.get_value(iter2, 1)

                    self.del_f_base(model.get_value(iter2, 0))

                    self.model.clear()
                    self.ins_tree()
                    self.selection.select_path((0,))

                if keyname == "i":
                    face = Mug()

                if keyname == "s":
                    self.save_cur()
        elif isinstance(widget, gtk.Entry):

            # next result is search (Viewer)
            if event.state & gtk.gdk.CONTROL_MASK:
                if keyname == "n" or keyname == "Cyrillic_te":
                    
                    if res_num < len(search_res) - 1:
                        res_num += 1
                        self.selection.select_path(search_res[res_num])
                        self.tv.scroll_to_cell(search_res[res_num])
                        self.tv.set_cursor_on_cell(search_res[res_num])

                # previous result is search (Viewer)
                if keyname == "p" or keyname == "Cyrillic_ze":
                    if res_num != 0:
                        res_num -= 1
                        self.selection.select_path(search_res[res_num])
                        self.tv.scroll_to_cell(search_res[res_num])
                        self.tv.set_cursor_on_cell(search_res[res_num])

    def entry_cb(self, event):
        """Callback for entry widg
           Look for word in results of primary search

        """
        
        # a_num, b_greek, c_clav, d_rus, e_desc, greek, beta, slav, source

        global search_res
        global res_num
        res_num = 0

        col_num = 6 # search betacode

        if self.search_col_sw == 0:
            col_num = 5 # search greek symbols
        elif self.search_col_sw == 1:
            col_num = 6 # search betacode
        elif self.search_col_sw == 2:
            col_num = 9 # search slavonic (hip)
        search = event.get_text()
        print "search", search

        data = [search]

        def find_match(model, path, iter, data):

            match_line = model.get_value(iter, col_num)
            if match_line.find(data[0]) >= 0:
                data.append(path)
        self.modelfilter.foreach(find_match, data)
        search_res = data[1:] # в начале - поисковое слово, потом список найденных paths
        if search_res:
            self.selection.select_path(search_res[0])
            self.tv.scroll_to_cell(search_res[0])
            print search_res
        else:
            print 'no match found'


    def save_cur(self):
        """Save current changes to base"""
        pass


    def del_f_base(self, num):

        conn = self.open_base()
        cur = conn.cursor()

        cur.execute("DELETE FROM " + tree.table_name + " WHERE a_num=:k", {"k": num})

        conn.commit()
        cur.close()

    def edit_base(self, command):

        conn = self.open_base()
        cur = conn.cursor()

        cur.execute(command)

        conn.commit()
        cur.close()

    def get_f_base(self, command):

        conn = self.open_base()
        cur = conn.cursor()

        cur.execute(command)
        res = cur.fetchall()

        cur.close()

        return res

    def ins_base(self, data):
        # data = (word_greek, word_slav, word_rus, description, source)
        
        conn = self.open_base()
        cur = conn.cursor()

        gr_line = data[0]
        gr_line = unicodedata.normalize('NFD', gr_line)

        for a in [u'\u0300', u'\u0342', u'\u0301', u'\u0314', u'\u0313']:
            gr_line = gr_line.replace(a, '')

        betacode = beta.revert_all(gr_line)

        rus_txt = russ.conv_str(data[1]).decode('utf')

#            a_num, b_greek, c_slav, d_rus, e_desc, greek, beta, slav, source
        command = 'insert into ' + tree.table_name + ' values (?,?,?,?,?,?,?,?,?)'
        cur.execute(command, [None, data[0], data[1], data[2], data[3], gr_line, betacode, rus_txt, data[4]]) # Do not write primary key!!!!

        conn.commit()
        cur.close()

        print 'Inserted: ' + ', '.join(data[1:]) + ' into base'
   
    def open_base(self):
        # should check if the base is already opened

        if self.b_name:
            base_p = self.b_name
        else:
            home = os.path.expanduser('~')
            base_p = os.path.join(home, 'coding/beta_dict')

        conn = sqlite3.connect(base_p)
        
#        cur = self.conn.cursor()

        return conn

    def close_base(self, cur):
        pass

    ########## Callbacks for Mug ##########33

    def manager_keys(self, widget, event):        
        """Callback for input widget"""

        keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & gtk.gdk.CONTROL_MASK:
            if keyname == "Return":
                self.get_stuff()

    def get_stuff(self, button=None):
        """Get data from input wid, prepare for inserting into base"""


        text1 = self.entry1.get_text()
        text1 = text1.decode('utf-8')
        text2 = self.entry2.get_text()
        text2 = text2.decode('utf-8')
        text3 = self.entry3.get_text()
        text3 = text3.decode('utf-8')
        st, en = self.textb.get_bounds()
        text4 = self.textb.get_text(st, en).decode('utf-8')
        text5 = self.entry4.get_text()
        text5 = text5.decode('utf-8')

        tree.model.clear()
        self.ins_base([text1, text2, text3, text4, text5])

        self.entry1.set_text("")
        self.entry2.set_text("")
        self.entry3.set_text("")
        self.entry4.set_text("")
        self.textb.set_text("")

        tree.ins_tree()


class Main_window(Engine):
    """Widget to view and edit base"""

    def __init__(self, base_name=None, table_name=None):
        Engine.__init__(self, base_name, table_name)

#        ###### Configuration ###########
#
#        self.config = ConfigParser.ConfigParser()
#        self.config.read(os.path.join(os.path.expanduser('~'), '.config', 'hiptools', 'betarc'))
#
#        if base_name:
#            self.b_name = base_name
#        else:
#            self.b_name = self.config.get('Paths', 'beta_path')
#
#        if table_name:
#            self.table_name = table_name
#        else:
#            self.table_name = self.config.get('Tables', 'beta_tab')
#
#        self.sl_conv = True # славянскую колонку - в юникод. TODO: Если хотим править в hip - False
#
#        combo_tmp = self.config.get('SearchOptions', 'default_search')
#
#        cmb_ls = ['Greek', 'Betacode', 'Slavonic']
#        for s in range(len(cmb_ls)):
#            if combo_tmp == cmb_ls[s]:
#                self.cmb_active = s # 0, 1 or 2 - for ComboBox
#                self.search_col_sw = s # 0, 1, 2 - for my search engine. Stupid, aye?
#        self.gr_font = self.config.get('Fonts', 'gr_font')
#        self.sl_font = self.config.get('Fonts', 'sl_font')
#        #################################

        window2 = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window2.set_resizable(True)
        window2.set_border_width(10)
        window2.set_size_request(850, 400)

        window2.set_title("Просмотр базы: " + self.b_name + "; Табл.: " + self.table_name)
        window2.set_border_width(0)
        window2.connect("destroy", destroy_cb) 

        box1 = gtk.VBox(False, 0)
        window2.add(box1)
        box1.show()
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        box3 = gtk.HBox(False, 0)
        box2.pack_start(box3, False, False, 5)
        box3.show()

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
                                # a_num, b_greek, c_clav, d_rus, e_desc, greek, beta, slav, source, hip
        self.model = gtk.ListStore(int, str, str, str, str, str, str, str, str, str) 
        self.tv = gtk.TreeView(self.model)
        self.selection = self.tv.get_selection()

        self.modelfilter = self.model.filter_new()
        self.tv.set_model(self.modelfilter)

        sw.add(self.tv)

        self.combo = gtk.combo_box_new_text()
        self.entry = gtk.Entry()
        
        cell1 = gtk.CellRendererText()
        cell2 = gtk.CellRendererText()
        cell3 = gtk.CellRendererText()
        cell4 = gtk.CellRendererText()

        cell1.set_property('editable', True)       
        cell1.set_property('font', self.gr_font)
        cell2.set_property('editable', True)       
        cell2.set_property('font', self.sl_font)
        cell3.set_property('editable', True)       
        cell3.set_property('font', 'Tahoma 12')       
        cell4.set_property('editable', True)       
        cell4.set_property('font', 'Tahoma 12')       

        # give extra arg (column num) to callback
        cell1.connect('edited', self.edited_cb, 1) 
        cell2.connect('editing-started', self.sl_edited_cb, 2) # Neat! Slavonic word in Unic when browsed, in Hip when edited
        cell2.connect('edited', self.edited_cb, 2)
        cell3.connect('edited', self.edited_cb, 3) 
        cell4.connect('edited', self.edited_cb, 4) 

        self.column1 = gtk.TreeViewColumn("Greek", cell1, text=1)
        self.column2 = gtk.TreeViewColumn("Slavic", cell2, text=2)
        self.column3 = gtk.TreeViewColumn("Russian", cell3, text=3)
        self.column4 = gtk.TreeViewColumn("Description", cell4, text=4)

        self.tv.append_column(self.column1)
        self.tv.append_column(self.column2)
        self.tv.append_column(self.column3)
        self.tv.append_column(self.column4)

        self.tv.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
        self.tv.set_search_column(1)

        sw.show_all()
        self.tv.show()
        box2.pack_start(sw)
        box3.pack_start(self.combo, True, True, 5)
        box3.pack_start(self.entry, True, True, 5)

        self.entry.connect('activate', self.entry_cb)
        self.entry.connect('key_press_event', self.on_key_press_event)

        for s in ['Greek', 'Betacode', 'Slavonic']:
            self.combo.append_text(s)

        self.combo.set_active(self.cmb_active)
        self.combo.show()
        self.entry.show()
        self.combo.connect("changed", self.toggler)       

        window2.show()
        self.tv.connect('key_press_event', self.on_key_press_event)

        self.ins_tree()
        self.entry.grab_focus()

class Mug(Engine):
    """Window to input new entries"""

    def __init__(self):
        Engine.__init__(self)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Insert info into base")
        self.window.set_border_width(10)
        self.window.set_size_request(500, 320)
        self.window.connect("key_press_event", self.manager_keys) 

        self.vbox = gtk.VBox(False, 0)
        self.entry1 = gtk.Entry()
        self.entry2 = gtk.Entry()
        self.entry3 = gtk.Entry()
        self.entry4 = gtk.Entry()

        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.tv = gtk.TextView()
        self.tv.set_editable(True)
        self.tv.set_accepts_tab(False)
        self.textb = self.tv.get_buffer()

        self.sw.add(self.tv)

        self.but = gtk.Button('Insert')
        
        self.vbox.pack_start(self.entry1, False, False, 1)
        self.vbox.pack_start(self.entry2, False, False, 1)
        self.vbox.pack_start(self.entry3, False, False, 1)
        self.vbox.pack_start(self.entry4, False, False, 1)
        self.vbox.pack_start(self.sw, False, False, 3)
        self.vbox.pack_end(self.but, False, False, 1)

        self.window.add(self.vbox)

        self.entry1.show()
        self.entry2.show()
        self.entry3.show()
        self.entry4.show()
        self.sw.show()
        self.tv.show()
        self.but.show()
        self.vbox.show()
        self.window.show()


#######################main########       
#argv = sys.argv

def main():
    gtk.main()
    return 0

from optparse import OptionParser
usage = "usage: %prog [options] word1 [word2] description"
parser = OptionParser(usage=usage)

#parser.add_option("-l", "--list", dest="list", action='store', help="Take list of words as an argument")
#parser.add_option("-c", "--create", dest="create", action='store_true', help="Create new base")

(options, args) = parser.parse_args()

data = []
#print "len:", len(args)

if args:
#    main_f = Engine(args[0])
    if len(args) < 2:
        tab = None
    else:
        tab = args[1]
    tree = Main_window(args[0], tab)
else:
    tree = Main_window()

main()
#if args:
#    main_f = Engine(args[0])
#    if len(args) < 2:
#        #tab = 'dictionary'
#        tab = None
#    else:
#        tab = args[1]
#    tree = Main_window(args[0], tab) # зачем запускаем Engine и Main_window раздельно?
#    main()
#else:
#    print "basename [tablename] is needed"

'''TODO: config?  self.search_col_sw - по умолчанию 'b' = Betacode. Ищем по транслитерации.

    TODO: в конфиге - путь к базе и название таблицы

    почини кнопку Save в Mug
'''
