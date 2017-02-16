#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''CLI модуль для работы с базами beta'''

import codecs
import re
import os
import sys

import types
import sqlite3
import logging
import unicodedata

from betacode import Beta
import write_utf
import russ_simp

Writer = write_utf.write_gen()
beta = Beta()
russ = russ_simp.Mn(True, True, True)

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", filename="beta_tools.log", filemode="w", level=logging.INFO)

class Base:
    """Main engine. Base handler"""

    def __init__(self, b_name=None):
        # crappy regex, have to fix
        self.reg = re.compile('^(.+?) (?:slav) (.+?) (?:desc) (.+?)$', re.U)
        self.white = re.compile(u'(\r|\n|\r\n)', re.M)

        self.cols = ["b_greek", "c_slav", "d_rus", "e_desc"]

        self.b_name = b_name

        self.so = re.compile(u'[Мм]ф', re.U)

    def create_base(self, tab_name='dictionary'):

        conn = sqlite3.connect(self.b_name)
        cur = conn.cursor()

        if tab_name:
#            command = "CREATE TABLE " + tab_name + " (a_num INTEGER PRIMARY KEY, b_greek TEXT, c_slav TEXT, d_rus TEXT, e_desc TEXT)"
            command = "CREATE TABLE " + tab_name + " (a_num INTEGER PRIMARY KEY, b_greek TEXT, c_slav TEXT, d_rus TEXT, e_desc TEXT, greek TEXT, beta TEXT, slav TEXT, source TEXT)"
            cur.execute(command)
        else:
            print 'no table name given, nothing is done'
        cur.close()

    def del_f_base(self, num):

        conn = self.open_base()
        cur = conn.cursor()

        cur.execute("DELETE FROM dictionary WHERE a_num=:k", {"k": num})

        conn.commit()
        cur.close()

    def edit_base(self, command):

        conn = self.open_base()
        cur = conn.cursor()

        cur.execute(command)

        conn.commit()
        cur.close()

    def get_f_base(self, command):
        '''technical utility for pr_base(), used in beta.py also'''

        conn = self.open_base()
        cur = conn.cursor()

        cur.execute(command)
        res = cur.fetchall()

        cur.close()

        return res

    def ins_base(self, data, tab_name='dictionary'):
        # data = (word_greek, word_slav, description)
        
        conn = self.open_base()
        cur = conn.cursor()
            
        cur.execute("INSERT INTO " + tab_name + " (b_greek, c_slav, d_rus, e_desc) VALUES (?,?,?,?);", data)

        conn.commit()
        cur.close()

        print 'Inserted: ' + ', '.join(data[1:]) + ' into base'
    
    def parse_txt(self, f_lines, tab_name='dictionary'):
        """Parse data from file"""

        for n in range(len(f_lines)):
#            data = self.reg.findall(line)[0]
            line = f_lines[n]
            line = line.strip()
            # commentaries (e.g. text already inserted into base)
            if line.startswith('#'):
                continue

            # clean new lines
            line = self.white.sub('', line)

            if '||' in line:
                data = line.split('||')
            elif '//' in line:
                data = line.split('//')
            else:
                print 'no delimiter in line', n
                logging.info('no delimiter in line %s', n)
                continue
            if len(data) > 4:
                print 'too many chunks in', n
                logging.info('too many chunks in %s', n)
            if len(data) < 4:
                print 'too few chunks in', n
                logging.info('too few chunks in %s', n)
#            for i in data:
#                print i.strip()
            else:
                self.ins_base(data, tab_name)
#                print 'OK in', n

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

#    def close_base(self, cur):
#        pass

    def pr_base(self, tab_name='dictionary'):
        """print base to file (dump text)"""

        command = "SELECT * FROM " + tab_name + " ORDER BY b_greek"
        rows = self.get_f_base(command)

        out_l = []

        for row in rows:
            itms = []

            for itm in [row[1], '||', row[2], '||', row[3], '||', row[4]]:
                n_itm = itm.replace('\n', '; ')
                n_itm = n_itm.strip()
                itms.append(n_itm)

            out_l.append(''.join(itms))
            out_l.append('\n')

        Writer.write_file('tmp', out_l)

#            print ''.join(itms)

#        print '\n'.join(out_l)

#            print itms[0], '=', itms[1], '=', itms[2], '=', itms[3]
#            print row[0], '=', row[1], '=', row[2], '=', row[3], '=', row[4]

#        print 'Inserted: ' + ', '.join(data[1:]) + ' into base'

#    def search_txt (self, word, tab_name='dictionary', num=0):
    def search_txt (self, word, tab_name='menologion', num=0):
        
        word = "\'%" + word + "%\'"
        command = "SELECT * FROM " + tab_name + " WHERE " + self.cols[int(num)] + " LIKE " + word
#        print command
        res = self.get_f_base(command)
        for ln in res:
            for l in range(len(ln)): 
                line = ln[l]
                if l != 0:
                    line = line.encode('utf8')

                print line

    def update_txt(self, row, col, text, tab_name='dictionary'):
        '''Update entry in the table'''

        command = "SELECT * FROM " + tab_name + " WHERE a_num=\"" + str(row) + "\""
        res = self.get_f_base(command)
        old_text = res[0][int(col)]
        new_text = ''.join([old_text, '; ', text])

        print new_text

        command = "UPDATE " + tab_name + " SET " + self.cols[int(col) - 1] + "=\"" + new_text + "\" WHERE a_num=\"" + str(row) + "\""
#        print command

    def glue_long_table(self):

        conn = sqlite3.connect('beta_dict_1.db')
        cur = conn.cursor()

#            a_num INTEGER PRIMARY KEY, b_greek TEXT, c_slav TEXT, d_rus TEXT, e_desc TEXT, greek TEXT, beta TEXT, slav TEXT, source TEXT
        command = 'select b_greek, c_slav, d_rus, e_desc from dictionary order by a_num'
        cur.execute(command)
        res = cur.fetchall()

        out = []
        for z in res:
            zz = list(z)
            zz.append('0')
            out.append(zz) # Златоуст. Толк на Матфея, 
        #TODO: отдельную табличку по источникам.


        command = 'select b_greek, c_slav, d_rus, e_desc from menologion order by a_num'
        cur.execute(command)
        res = cur.fetchall()

        for z in res:
            zz = list(z)
            zz.append('1')
            out.append(zz) # Минеи

        cur.close()
        ################# test ##########
#        cnt = 1
#        for i in out:
#            logging.info('num %s', cnt)
#            for x in i:
#                if x and not type(x) == types.IntType:
#                    x = x.encode('utf-8')
#                logging.info('entry %s', x)
#            cnt += 1
        #################

        conn = sqlite3.connect(self.b_name) # new base
        cur = conn.cursor()
        cnt = 1
        for x in range(len(out)):
            i = out[x]

#            logging.info('num = %s, len(i) = %s', num, len(i))
            gr_line = i[0]
            gr_line = unicodedata.normalize('NFD', gr_line)

            for a in [u'\u0300', u'\u0342', u'\u0301', u'\u0314', u'\u0313']:
                gr_line = gr_line.replace(a, '')
            betacode = beta.revert_all(gr_line)
            rus_txt = russ.conv_str(i[2]).decode('utf')

#            logging.info('num %s gr %s, sl %s, ru %s, de %s', cnt, i[0], i[1], i[2], i[3])
#            logging.info('num %s', cnt)
#            logging.info('GR %s, BE %s, SL %s, SRC %s', gr_line, betacode, rus_txt, i[4])

#            a_num, b_greek, c_slav, d_rus, e_desc, greek, beta, slav, source
            command = 'insert into common values (?,?,?,?,?,?,?,?,?)'
            cur.execute(command, [None, i[0], i[1], i[2], i[3], gr_line, betacode, rus_txt, i[4]]) # Do not write primary key!!!!
            conn.commit()
            cnt += 1

        cur.close()

#######################main########       

if __name__ == '__main__':

    from optparse import OptionParser
    usage = "usage: %prog [options] word1 [word2] description"
    parser = OptionParser(usage=usage)

#parser.add_option("-l", "--list", dest="list", action='store', help="Take list of words as an argument")
    parser.add_option("-c", "--create", dest="create", action="store_true", help="Create new base")
    parser.add_option("-p", "--print_b", dest="print_b", action="store_true", help="Print base entries as formatted text into file")
    parser.add_option("-r", "--read", dest="read", action="store_true", help="Read text from file, parse and insert into base")
    parser.add_option("-l", "--line", dest="line", action="store_true", help="Read text from string, parse and insert into base")
    parser.add_option("-s", "--search", dest="search", action="store_true", help="Read text from string, parse and insert into base")
    parser.add_option("-u", "--update", dest="update", action="store_true", help="Update text in base: table name, text, row, col")
    parser.add_option("-t", "--table", dest="table", action="store_true", help="make table from data")

    (options, args) = parser.parse_args()

    data = []
#print "len:", len(args)

    if args:
#    main_f = Base()
#
#    if options.list:
#        res = main_f.fill_base_auto(options.list)
#    else:
#        for ar in args:
#            ar = ar.decode('utf-8')
#            data.append(ar)
#        res = main_f.ins_base(data)
        if options.create:
            main_f = Base(args[0])
            # needs table name as an argument
            main_f.create_base(args[1])
        elif options.print_b:
            # print base entries into text file
            main_f = Base(args[0])
            main_f.pr_base(args[1])
        elif options.read:
            # read file,
            # isert formatted lines into base 
            # (separator: // or ||)
            # args: 0=base, 1=tab, 2=file_name

            main_f = Base(args[0])
            fp = codecs.open(args[2], "rb", "utf-8")
            f_lines = fp.readlines()
            fp.close()

            # strings and table name to parse 
            main_f.parse_txt(f_lines, args[1])

        elif options.line:
            # isert formatted line into base (separator: // or ||)
            # args: 0=base, 1=tab, 2=string
            main_f = Base(args[0])
            string1 = args[2].decode('utf8')
            # str and table name to parse 
            main_f.parse_txt([string1,], args[1])

        elif options.search:
            # args: 0=dict, 1=tab, 2=word, 3=col
            main_f = Base(args[0])
            string1 = args[2].decode('utf8')
            if len(args) < 4:
                col = "0"
            else:
                col = args[3]
            # search word, dict, column
            main_f.search_txt(string1, args[1], col)
        
        elif options.update:
            # update entry in the table (not tested)
            main_f = Base(args[0])
            text = args[2].decode('utf8')
            # row, col, text, tab_name:
            main_f.update_txt(args[3], args[4], text, args[1])
        elif options.table:
            main_f = Base(args[0])
#            main_f.make_table()
            main_f.glue_long_table()

        else:
            print 'no options, exiting'
    else:
        print 'no args, exiting'
#        main_f = Base()

'''TODO: объединить таблицы dictionary и menologion:

out = []
for tab in [dictionary, menologion]    
    select * from tab
    res = cur.fetchall()
    out.extend(res)
Идея: добавить колонку source (Злат. Мф или Минея ...)
    if 'Мф' in e_desc[i]:
        source = e_desc[i]

Идея: при заполнении таблицы три последних столбца (greek, beta, slav) заполняются автоматически (при добавлении в базу)
также автоматически конвертация hip->unicode

'''
#    def fill_base_auto(self, f_name):
#        """Parse data from file"""
#
#        fp = codecs.open(f_name, "rb", "utf-8")
#        f_lines = fp.readlines()
#        fp.close()
#
#        for line in f_lines:
#            data = self.reg.findall(line)[0]
#
#            conn = self.open_base()
#            cur = conn.cursor()
#            cur.execute("insert into dictionary values (data[0], data[1], data[2])")
#            conn.commit()
#            cur.close()
