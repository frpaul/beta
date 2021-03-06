#! /usr/bin/python
# -*- coding: utf-8 -*-
"""A convertor from HIP to UCS-8, UTF-8. 

"""
 
class Repl:
    def __init__(self):
        
        #Список замен hip - ucs8
        self.ucs_lst = [                        
                        # ударения и придыхания
                        ("='", u'4'), 
                        ('=`', u'5'), 
                        ("'", u'1'), 
                        ('`', u'2'), 
                        ('=', u'3'), 
                        ('^', u'6'), 
                        ('~', u'7'),
                         # Заглавные буквы с надрстроч
                        ('_Я', u'JА'), 
                        ('Jа', u'JА'), # приведение к универс виду
                        ('JА4', u'\u040b'), 
                        ('JА3', u'\u004b'), 
                        ('JА1', u'\u042f\u007e'), 
                        ('JА', u'J\u0410'), # приведение к универсальному

                        ("А4", u'\u0403'), 
#                        ('А5`', u'J\u044c'), 
                        ('А1', u'\u0410\u007e'), 
                        ('А2', u'\u0410\u0040'), 
                        ('А3', u'\u0490'), 

                        ('Е4', u'\u0415\u0024'), 
                        ('Е3', u'\u0415\u0023'), 
                        ('Е1', u'\u0415\u007e'), 
                        ('Е2', u'\u0415\u0040'), 

                        ('И4', u'\u0418\u0024'), 
                        ('И3', u'\u0418\u0023'), 
                        ('И1', u'\u0418\u007e'), 
                        ('И2', u'\u0418\u0040'), 

                        ('I4', u'\u0408'), 
                        ('I3', u'\u0407'), 
                        ('I1', u'\u0407\u007e'), 

                        ('_О4', u'\u040f'),    # _О
                        ('_О3', u'\u004e'),    # _О
                        ('_О', u'\u004f'),    # _О
                        ('О4', u'\u041e\u0024'), 
                        ('О3', u'\u041e\u0023'), 
                        ('О1', u'\u041e\u007e'), 
                        ('О2', u'\u041e\u0040'), 

                        ('_W4', u'\u0051'), 
                        ('_W', u'\u0051'), 
                        ('_w4', u'\u0071'), 
                        ('_w', u'\u0071'), 

                        ('W\т', u'\u0054'), 

                        ('W4', u'\u0057\u0024'), 
                        ('W3', u'\u040a'), 
                        ('W1', u'\u0057\u007e'), 
                        ('W2', u'\u0057\u0040'), 

                        ('О_у4', u'\u040c'),    # О_у с надстроч 
                        ('О_у3', u'\u040e'), 

#                        ('У', u'\u044c'), 
#                        ('У', u'\u044c'), 
#
                        ('Ю4', u'\u042e\u0024'), 
                        ('Ю3', u'\u042e\u0023'), 
                        ('Ю1', u'\u042e\u007e'), 
                        ('Ю2', u'\u042e\u0040'), 


                        ('Я4', u'\u005a'), 
                        ('Я3', u'\u0409'), 
                        ('Я1', u'\u005a\u007e'), 
                        ('Я2', u'\u005a\u0040'), 

                       # букво-титла
                        ('\\ъ', u'8'),
                        ('\\в', u'\u002b'),
                        ('\\х', u'\u003c'),
                        ('\\н', u'\u003d'),
                        ('\\р', u'\u003e'),
                        ('\\ч', u'\u003f'),
                        ('\\о', u'\u0062'),
                        ('\\с', u'\u0063'),
                        ('\\д', u'\u0064'),
                        ('\\г', u'\u0067'),
                        ('\\з', u'\u20ac'),
                        ('w\\т', u'\u0074'),
#                        ('jа', u'\u044f'),
                        ('jа', u'zz'),

                        # маскируем дифтонги, сочетания с i
#                        ('о_у4', u'\u045c'),              # о_у
#                        ('о_у3', u'\u045e'),              # о_у
                        ('о<у>', u'о_у'),              # о_у
                        ('о_у', u'\u0075'),              # о_у
                        ('_у', u'\u00b5'),          # ук 
                        ('а4', u'\u0453'),          # аз
                        ('а1', u'\u0061'),
                        ('а2', u'\u0041'),
                        ('а3', u'\u0491'),
                        ('а6', u'\u2020'),
                        ('а7', u'\u2116'),

#                        ('_е', u''), 
                        ('_е1', u'\u0454'u'1'), 
                        ('_е3', u'\u0454'u'3'), 
                        ('_е4', u'\u0454'u'4'), 
                        ('_е6', u'\u0454'u'6'), 
                        ('_е7', u'\u0454'u'7'), 
                        ('_е', u'\u0454'), 
                        ('е1', u'\u0065'),
                        ('е2', u'\u0045'),
                        ('_Е', u'\u0415'), 

                        ('я5', u'\u007c'),          # юс малый 
#                        ('я1', u'\u0073'),    # показывает s вместо юникода. PyGTK?
                        ('я1', u'kk'),    
#                        ('я2', u'\u0053'),  # = S (Осторожно! конвертиться в Зело!)
                        ('я2', 'L'),  # = S 
                        ('я3', u'\u0459'), 
                        ('я6', u'\u2030'), 
                        ('я', u'\u007a'), 
                        ('zz', u'\u044f'),
                        ('i4', u'r4'), 
                        ('i5', u'r5'), 
                        ('i3', u'r3'), 
                        ('i1', u'r1'), 
                        ('i2', u'r2'), 
                        ('_i', u'_r'), 
                        ('_кс', u'x'),   # кси
                        ('_пс', u'p'),   # пси
                        ('_Кс', u'\u0058'),   # кси
                        ('_Пс', u'\u0050'),   # пси
#                        # basic conversion                        
                        ('s', u'\u0455'),
                        ('S', u'\u0405'),
                        ('L', u'\u0053'), # юс с тупым ударением (2) 
                        ('kk', u'\u0073'),   #  подстановка для я1 
                        ("jь1", u'\u0451'),    # ять
                        ('jь2', u'\u0401'),
                        ('jь6', u'\u044d^'),
                        ('jь', u'\u044d'),
                        ("у1", u'\u0079'),    # у лигатурное с ударением
                        ("у2", u'\u0059'),
                        ("у6", u'\u007b'),     
                        ('<е>', u'\u0454'),   # вытянутое е
                        ('_w', u'\u045a'),
                        ('_О4', u'\u040f'),    # _о
                        ('_о4', u'\u045f'),    # _о
                        ('_О3', u'\u004e'),    # _о
                        ('_о3', u'\u006e'),    # _о
                        ('_О', u'\u004f'),    # _о
                        ('_о', u'\u006f'),    # _о
                        ('<О>4', u'\u040f'),    # _о
                        ('<о>4', u'\u045f'),    # _о
                        ('<О>3', u'\u004e'),    # _о
                        ('<о>3', u'\u006e'),    # _о
                        ('<О>', u'\u004f'),    # _о
                        ('<о>', u'\u006f'),    # _о
                        ('v"', u'm'),
                        ('r4', u'\u0458'),         # i='
                        ('r3', u'\u0457'),         # i=
                        ('r1', u'j'),
                        ('r2', u'J'),
                        ('i', u'\u0456'),          # i с двумя точками (default)
                        ('_r', u'\u0069'),         # _i - i без точек 
                        ('u3', u'\u045e'),         # о_у=
                        ('u4', u'\u045c'),         # о_у='
                        ('@', u'\u00b0')]
                         # конвертируем киноварь в "костыльные" метки
#                        ('%<', u'\1'),
#                        ('%>', u'\2')]

        # Список замен hip - unicode csl
        self.unic_csl_lst = [('_Е', u'\u0415'),
                        ('_е', u'\u0454'), 
                        ('<е>', u'\u0454'),   # вытянутое е
                        ('_Я', u'JА'), 

                        ('i=\'', u'\u0456\u0486\u0301'),            # i с диакритикой
                        ('i=`', u'\u0456\u0486\u0300'),
                        ('i\'', u'\u0456\u0301'),
                        ('i`', u'\u0456\u0300'),
                        ('i=', u'\u0456\u0486'),
                        ('i^', u'\u0456\u0311'),
                        ('_i', u'\u0456'),            # i в числах
                        ('i~', u'\u0456\u0483'),            # i в словах под титлом

                        ('i', u'\u0457'),            # i с двумя точками

                        # ударения и придыхания
                        ("='", u'\u0486\u0301'), 
                        ('=`', u'\u0486\u0300'), 
                        ("'", u'\u0301'), 
                        ('`', u'\u0300'), 
                        ('=', u'\u0486'), 
                        ('^', u'\u0311'), 
                        ('~', u'\u0483'),
                         # Я йотированн и юс малый
                        ('Jа', u'\ua656'), # приведение к универс виду
                        ('JА', u'\ua656'), 
                        ('jа', u'\ua657'),
                        ('Я', u'\u0466'),
                        ('я', u'\u0467'),

                        ('W\\т', u'\u047e'), 
                        ('w\\т', u'\u047f'),
                        
                        ('_W', u'\u047c'),
                        ('_w', u'\u047d'),

                        ('W', u'\u0460'),
                        ('w', u'\u0461'),

                        ('_О', u'\u047a'),    # _о
                        ('_о', u'\u047b'),    # _о
                        ('<о>', u'\u043e'),    # _о

                        ('F', u'\u0472'),
                        ('f', u'\u0473'),


                       # букво-титла
                        ('\\ъ', u'\u2e2f'),
                        ('\\б', u'\u2de0\u0487'),
                        ('\\в', u'\u2de1\u0487'),
                        ('\\г', u'\u2de2\u0487'),
                        ('\\д', u'\u2de3'),
                        ('\\ж', u'\u2de4'),
                        ('\\з', u'\u2de5'),
                        ('\\к', u'\u2de6\u0487'),
                        ('\\л', u'\u2de7\u0487'),
                        ('\\м', u'\u2de8'),
                        ('\\н', u'\u2de9\u0487'),
                        ('\\о', u'\u2dea\u0487'),
                        ('\\п', u'\u2deb\u0487'),
                        ('\\р', u'\u2dec\u0487'),
                        ('\\с', u'\u2ded\u0487'),
                        ('\\т', u'\u2dee'),
                        ('\\х', u'\u2def\u0487'),
                        ('\\ц', u'\u2df0\u0487'),
                        ('\\ч', u'\u2df1\u0487'),
                        ('\\ш', u'\u2df2\u0487'),
                        ('\\щ', u'\u2df3\u0487'),
                        ('\\f', u'\u2df4\u0487'),

                        # дифтонги, сочетания с i
                        ('о<у>', u'\u0479'),              # о_у
                        ('о_у', u'\u0479'),              # о_у
                        ('О_у', u'\u0478'),              # о_у
                        ('<у>', u'\u0443'),          # ук 
                        ('_у', u'RR'),          # ук 
                        ('У', u'\ua64a'),            # y лигатурное
                        ('у', u'\ua64b'),            # y лигатурное
                        ('RR', u'\u0443'),          # ук 


#                        ('_i', u'_r'), 
                        ('_Кс', u'\u046e'),   # кси
                        ('_кс', u'\u046f'),   # кси
                        ('_Пс', u'\u0470'),   # пси
                        ('_пс', u'\u0471'),   # пси
#                        # basic conversion                        
                        ('S', u'\u0405'),
                        ('s', u'\u0455'),
                        ('Jь', u'\u0462'),
                        ('JЬ', u'\u0462'),
                        ('jь', u'\u0463'),
                        ('V"', u'\u0476'),
                        ('v"', u'\u0477'),
                        ('V', u'\u0474'),
                        ('v', u'\u0475'),

                        ('#', u'\u0482'),
                        ('@', u'\ua67e')]

                         # конвертируем киноварь в "костыльные" метки
#                        ('%<', u'\1'),
#                        ('%>', u'\2')]

        # regular unicode convertion
        self.unic_lst = [('_Е', u'\u0415'),
                        ('_е', u'\u0454'), 
                        ('<е>', u'\u0454'),   # вытянутое е
                        ('_Я', u'JА'), 

#                        ('i=\'', u'\u0456\u0486\u0301'),            # i с диакритикой
#                        ('i=`', u'\u0456\u0486\u0300'),
#                        ('i\'', u'\u0456\u0301'),
#                        ('i`', u'\u0456\u0300'),
#                        ('i=', u'\u0456\u0486'),
#                        ('i^', u'\u0456\u0311'),
#                        ('_i', u'\u0456'),            # i в числах
#                        ('i~', u'\u0456\u0483'),            # i в словах под титлом

#                        ('i', u'\u0457'),            # i с двумя точками

                        # ударения и придыхания
                        ("='", u''), 
                        ('=`', u''), 
                        ("'", u'\u0301'), 
                        ('`', u'\u0300'), 
                        ('=', u''), 
                        ('^', u'\u0311'), 
                        ('~', u'\u0483'),
                         # Я йотированн и юс малый
                        ('Jа', u'\ua656'), # приведение к универс виду
                        ('JА', u'\ua656'), 
                        ('jа', u'\ua657'),
                        ('Я', u'\u0466'),
                        ('я', u'\u0467'),

                        ('W\\т', u'\u047e'), 
                        ('w\\т', u'\u047f'),
                        
                        ('_W', u'\u047c'),
                        ('_w', u'\u047d'),

                        ('W', u'\u0460'),
                        ('w', u'\u0461'),

                        ('_О', u'\u047a'),    # _о
                        ('_о', u'\u047b'),    # _о

                        ('F', u'\u0472'),
                        ('f', u'\u0473'),


                       # букво-титла
                        ('\\ъ', u'\u2e2f'),
                        ('\\б', u'\u2de0'),
                        ('\\в', u'\u2de1'),
                        ('\\г', u'\u2de2'),
                        ('\\д', u'\u2de3'),
                        ('\\ж', u'\u2de4'),
                        ('\\з', u'\u2de5'),
                        ('\\к', u'\u2de6'),
                        ('\\л', u'\u2de7'),
                        ('\\м', u'\u2de8'),
                        ('\\н', u'\u2de9'),
                        ('\\о', u'\u2dea'),
                        ('\\п', u'\u2deb'),
                        ('\\р', u'\u2dec'),
                        ('\\с', u'\u2ded'),
                        ('\\т', u'\u2dee'),
                        ('\\х', u'\u2def'),
                        ('\\ц', u'\u2df0'),
                        ('\\ч', u'\u2df1'),
                        ('\\ш', u'\u2df2'),
                        ('\\щ', u'\u2df3'),
                        ('\\f', u'\u2df4'),

                        # дифтонги, сочетания с i
                        ('о<у>', u'\u0479'),              # о_у
                        ('о_у', u'\u0479'),              # о_у
                        ('<у>', u'\u0443'),          # ук 
                        ('_у', u'\u0443'),          # ук 
                        ('У', u'\ua64a'),            # y лигатурное
                        ('у', u'\ua64b'),            # y лигатурное


#                        ('_i', u'_r'), 
                        ('_Кс', u'\u046e'),   # кси
                        ('_кс', u'\u046f'),   # кси
                        ('_Пс', u'\u0470'),   # пси
                        ('_пс', u'\u0471'),   # пси
#                        # basic conversion                        
                        ('S', u'\u0405'),
                        ('s', u'\u0455'),
                        ('Jь', u'\u0462'),
                        ('JЬ', u'\u0462'),
                        ('jь', u'\u0463'),
                        ('V"', u'\u0476'),
                        ('v"', u'\u0477'),

                        ('#', u'\u0482'),
                        ('@', u'\ua67e')]

                         # конвертируем киноварь в "костыльные" метки
#                        ('%<', u'\1'),
#                        ('%>', u'\2')]

        #Список замен ucs8 - hip
        self.b_ucs_lst = [                        
                       # букво-титла
                        (u'\\ъ', u'8'),
                        (u'\\в', u'\u002b'),
                        (u'\\х', u'\u003c'),
                        (u'\\н', u'\u003d'),
                        (u'\\р', u'\u003e'),
                        (u'\\ч', u'\u003f'),
                        (u'\\о', u'\u0062'),
                        (u'\\с', u'\u0063'),
                        (u'\\д', u'\u0064'),
                        (u'\\г', u'\u0067'),
                        (u'\\з', u'\u20ac'),
                        (u'w\\т', u'\u0074'),

                        # ударения и придыхания
                        (u"'", u'1'), 
                        (u'\'', u'\u007e'), # вариант острого ударения в позиции тильды
                        (u'`', u'2'), 
                        (u'=', u'3'), 
                        (u"='", u'4'), 
                        (u'=`', u'5'), 
                        (u'^', u'6'), 
                        (u'~', u'7'),
                        # дополнительные надстрочники
                        (u'`', u'\u0040'), 
                        (u'=', u'\u0023'), 
                        (u'=\'', u'\u0024'), 
                        (u'=`', u'\u0025'), 
                        (u'~', u'\u0026'), 
                        


                         # Заглавные буквы с надрстроч
#                        (u'_Я', u'JА'), 
#                        (u'Jа', u'JА'), # приведение к универс виду
                        (u'$$', u'J\u0410'), # JA - временная замена из-за I

                        (u"А=\'", u'\u0403'), 
##                        u('А5`', u'J\u044c'), 
#                        (u'А\'', u'\u0410\u007e'), 
#                        (u'А`', u'\u0410\u0040'), 
                        (u'А=', u'\u0490'), 
#
#                        (u'Е=\'', u'\u0415\u0024'), 
#                        (u'Е=', u'\u0415\u0023'), 
#                        (u'Е\'', u'\u0415\u007e'), 
#                        (u'Е`', u'\u0415\u0040'), 
#
#                        (u'И=\'', u'\u0418\u0024'), 
#                        (u'И=', u'\u0418\u0023'), 
#                        (u'И\'', u'\u0418\u007e'), 
#                        (u'И`', u'\u0418\u0040'), 

                        (u'I=\'', u'\u0408'), 
                        (u'I=', u'\u0407'), 
#                        (u'I\'', u'\u0407\u007e'), 

#                        (u'_W=\'', u'\u0051'), 
                        (u'_W', u'\u0051'), 
#                        (u'_w=\'', u'\u0071'), 
                        (u'_w', u'\u0071'), 

                        (u'W\т', u'\u0054'), 

#                        (u'W=\'', u'\u0057\u0024'), 
                        (u'W=', u'\u040a'), 
#                        (u'W\'', u'\u0057\u007e'), 
#                        (u'W`', u'\u0057\u0040'), 

                        (u'О_у=\'', u'\u040c'),    # О_у с надстроч 
                        (u'О_у=', u'\u040e'), 
#
##                        u('У', u'\u044c'), 
##                        u('У', u'\u044c'), 
##
#                        (u'Ю4', u'\u042e\u0024'), 
#                        (u'Ю3', u'\u042e\u0023'), 
#                        (u'Ю1', u'\u042e\u007e'), 
#                        (u'Ю2', u'\u042e\u0040'), 
#
#
#                        (u'Я=\'', u'\u005a'), 
                        (u'Я=', u'\u0409'), 
                        (u'Я', u'\u005a'), 
#                        (u'Я1', u'\u005a\u007e'), 
#                        (u'Я2', u'\u005a\u0040'), 
#
#
#                        # маскируем дифтонги, сочетания с i
                        (u'о_у=\'', u'\u045c'),              # о_у
                        (u'о_у=', u'\u045e'),              # о_у
#                        (u'о<у>', u'о_у'),              # о_у
                        (u'о_у', u'\u0075'),              # о_у
                        (u'_у', u'\u00b5'),          # ук 

                        (u'а=\'', u'\u0453'),          # аз
                        (u'а\'', u'\u0061'),
                        (u'а`', u'\u0041'),
                        (u'а=', u'\u0491'),
                        (u'а^', u'\u2020'),
                        (u'а~', u'\u2116'),
#
##                        u('_е', u''), 
#                        (u'_е1', u'\u0454'u'1'), 
#                        (u'_е3', u'\u0454'u'3'), 
#                        (u'_е4', u'\u0454'u'4'), 
#                        (u'_е6', u'\u0454'u'6'), 
#                        (u'_е7', u'\u0454'u'7'), 
#                        (u'_е', u'\u0454'), 
                        (u'е\'', u'\u0065'),
                        (u'е`', u'\u0045'),
#                        (u'_Е', u'\u0415'), 

                        (u'i=\'', u'\u0458'),         # i='
                        (u'_i~', u'\u2039'),         # _i~
                        (u'_i', u'\u0069'),         # _i
                        (u'i=', u'\u0457'),         # i=
                        # и не трогай больше! Оно только похоже на обычное i!
                        (u'i', u'\u0456'),         # (в юникоде - обычная латинская i)

                        (u'i\'', u'j'),
                        (u'I\'', u'J'),
                        (u'jа', u'\u044f'),
##                        (u'я', u'z'),

                        (u'JА=\'', u'\u040b'), 
                        (u'JА=', u'\u004b'), 
#                        (u'JА\'', u'\u042f\u007e'), 
                        (u'JA', u'$$'), # приведение к универсальному
#
                        (u'я', u'\u007a'), 
                        (u'я=`', u'\u007c'),          # юс малый 
                        (u'я\'', u'\u0073'),    # показывает s вместо юникода. PyGTK?
#                        (u'я1', u'kk'),    # показывает s вместо юникода. PyGTK?
                        (u'я`', u'\u0053'), 
                        (u'я=', u'\u0459'), 
                        (u'я^', u'\u2030'), 

                        (u'_кс', u'x'),   # кси
                        (u'_пс', u'p'),   # пси
                        (u'_Кс', u'\u0058'),   # кси
                        (u'_Пс', u'\u0050'),   # пси
##                        # basic conversion                        
                        (u"jь'", u'\u0451'),    # ять с острым ударением
                        (u'jь`', u'\u0401'),    # ять с тупым ударением
                        (u'jь', u'\u044d'),

                        (u"у\'", u'\u0079'),    # у лигатурное с ударением
                        (u"у`", u'\u0059'),
                        (u"у^", u'\u007b'),

                        (u'_е', u'\u0454'),   # вытянутое е
                        (u'_w', u'\u045a'),
                        (u'_О=\'', u'\u040f'),    # _о
                        (u'_о=\'', u'\u045f'),    # _о
                        (u'_О=', u'\u004e'),    # _о
                        (u'_о=', u'\u006e'),    # _о
                        (u'_О', u'\u004f'),    # _о
                        (u'_о', u'\u006f'),    # _о

                        (u'v"', u'\u006d'),
                        (u'v\\г', u'\u0452'),         # ижица с выносным "г"
                        (u'v\'', u'\u0402'),

                        ('s', u'\u0455'),  # не отличается внешне, но это разные позиции
#                        (u'u3', u'\u045e'),         # о_у=
#                        (u'u4', u'\u045c'),         # о_у='
#                        (u'jа', u'\u044f'),
                        (u'@', u'\u00b0')]
                         # конвертируем киноварь в "костыльные" метки
#                        ('%<', u'\1'),
#                        ('%>', u'\2')]

    def __call__(self, S, uni='ucs'):
        # создаем список кортежей по 2 эл. из двух строк
        # текст на входе д.б уже конвертирован в utf8!
        self.S = S
        if uni == 'uni':
            work_ls = self.unic_lst
        elif uni == 'uni_csl':
            work_ls = self.unic_csl_lst
        elif uni == 'b_csl':
        # 'backwards' ucs conversion: ucs8 -> hip
            for i in self.b_ucs_lst:
                src = i[1]#.encode('utf8')
                repl = i[0]#.encode('utf8')
#                print src, repl
                self.S = self.S.replace(src, repl)
            return self.S
        else:
        # 'strait' ucs conversion: hip -> ucs8
            work_ls = self.ucs_lst

        for i in work_ls:
#            sear = i[0].encode('utf8')
            repl = i[1].encode('utf8')
            self.S = self.S.replace(i[0], repl) 
 
        return self.S

if __name__ == "__main__":
#    txt = 'проба пjьра о_у=бw'
    txt = '_е=\'сть свеж<е>е'
    conv = Repl()
    print conv(txt)

# TODO: нужен фильтр для чисел _ук~д
# надо вынести фильтры в отдельные xml? файлы
