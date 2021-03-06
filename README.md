# beta
beta.py - греко-славяно-русский словарь.

## Краткое описание:

Программа создана для редактирования словаря греко-церковнославянско-русских соответствий. 
Есть возможность осуществлять поиск по базе на греческом, церковнославянском 
и русском языках.

На этапе создания этого репозитория, в базе находится около 200 значений.

## Инструкция:

Верхнее меню - для выбора режима поиска.

Колонки в окне записей:

* Греческое слово
* Славянский перевод
* Русский перевод
* Комментарий (описание) - примеры из текста 

## Основные функции программы:

* поиск по греческому слову (utf-8)
* поиск по Betacode (латинская транслитерация греческого слова). 
* поиск по славянскому переводу (русская транслитерация славянского слова).

### Пример поисковых запросов: 

* греческий (utf-8) - набирать следует без ударений и предыханий: χαλεπος
* betacode: calepoj => χαλεπός

θ = q

η = h

ς = j

σ = s

υ = u

ω = w

ξ = x

ψ = y

* Набор славянских слов - в русской транслитерации. Напр: яко той есть бог нашъ = ꙗ҆́кѡ то́й є҆́сть бг҃ъ на́шъ.

Переключение между режимами поиска осуществляется с помощью выпадающего меню вверху главного окна.

Редактирование записей в базе осуществляется непосредственно в главном окне, кликом на редактируемом поле.

При редактировании славянского текста (2 колонка) происходит замена юникодного представления на HIP для облегчения редактирования.

Внесение новых записей осуществляется нажатием **Ctrl+i**. 
При этом появляется меню ввода:

Греческое слово

Славянский перевод

Русский перевод

Источник (книга) - вводим номер

(Заняты: 0 - Толкование Златоуста на Ев от Матфея, 1 - Menologion, 2 - Orologion)

Описание (примеры из текстов)

Запись заполненных данных в базу осуществляется после нажатия **Ctrl+Enter** в меню ввода

Удаление записи из базы осущеествляется нажатием **Ctrl+d** в основном окне

Просьба к пользователям делиться результатами работы! База будет пополняться в любом случае, но вместе мы сможем сделать гораздо больше.
