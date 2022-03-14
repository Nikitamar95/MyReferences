# -*- coding: utf-8 -*-
#
#  String_preparing.py
#
#  Copyright 2022 Nikita Marchenko
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from String_convertion import *
from Functions_for_string import *
from Service_arrays import *


# Библиотека для транслитерации https://pypi.org/project/iuliia/
import iuliia
# Библиотека для перевода https://pypi.org/project/translate/
from translate import Translator


def String_preparing(main_string):

    # Поиск авторов
    find_authors = Find_Authors(main_string)  # см. в Functions_for_string.py
    main_string = find_authors[0]
    authors_arr = find_authors[1]

    # Поиск Названия
    find_title = Find_Title(main_string)
    main_string = find_title[0]
    title = find_title[1]

    # Поиск названия сборника/журнала
    find_name_of_compilation_or_journal = Find_name_of_compilation_or_journal(main_string)
    main_string = find_name_of_compilation_or_journal[0]
    name_of_compilation_or_journal = find_name_of_compilation_or_journal[1]

    # Поиск редакторов
    find_editors = Find_Editors(main_string)
    main_string = find_editors[0]
    editors_arr = find_editors[1]
        
    # Поиск города и издательства
    find_city_and_publishing_house = Find_city_and_publishing_house(main_string)
    main_string = find_city_and_publishing_house[0]
    city = find_city_and_publishing_house[1]
    publishing_house = find_city_and_publishing_house[2]

    # Поиск года
    find_a_year = Find_a_year(main_string)
    main_string = find_a_year[0]
    year = find_a_year[1]
        
    # Поиск номера
    find_a_number = Find_a_numder(main_string)
    main_string = find_a_number[0]
    number = find_a_number[1]
        
    # Поиск тома
    find_a_foliant = Find_a_foliant(main_string)
    main_string = find_a_foliant[0]
    foliant = find_a_foliant[1]
        
    # Поиск страниц
    pages = Find_pages(main_string)

    # Перевод и транслитерация

    # Введение переменных и списков
    authors_arr_translit = []
    editors_arr_translit = []
    publishing_house_translit = ""
    title_translit = ""
    name_of_compilation_or_journal_translit = ""
    title_translated = ""
    new_authors_arr = []
    # Транслитерация авторов, редакторов и названия
    # Поиск духовенства в спаске авторов и транслитерация
    for i in range(len(authors_arr)):
        if authors_arr[i] in cleargy_dict.keys():
            authors_arr[i] = cleargy_dict[authors_arr[i]]
    # Слияние фамилии и имени автора и его сана в один элемент списка
    for i in range(len(authors_arr)):
        if authors_arr[i] in cleargy_arr or authors_arr[i] in cleargy_dict.values():
            new_name_of_the_cleric = authors_arr[i-1] + ", " + authors_arr[i]
            new_authors_arr.pop()
            new_authors_arr.append(new_name_of_the_cleric)
        else:
            new_authors_arr.append(authors_arr[i])
    authors_arr = new_authors_arr
    for i in authors_arr:
        authors_arr_translit.append(iuliia.translate(i, schema=iuliia.ALA_LC_ALT))
    for i in editors_arr:
        editors_arr_translit.append(iuliia.translate(i, schema=iuliia.ALA_LC_ALT))  # Транслитерированные редакторы
    title_translit = iuliia.translate(title, schema=iuliia.ALA_LC_ALT)
    name_of_compilation_or_journal_translit = iuliia.translate(name_of_compilation_or_journal, schema=iuliia.ALA_LC_ALT)
    if city == "М.":  # Транслитерированный город с исключениями
        city_translit = "Moscow"
    elif city == "СПб." or city == "Спб.":
        city_translit = "St. Petersburg"
    elif city == "Л.":
        city_translit = "Leningrad"
    else:
        city_translit = iuliia.translate(city, schema=iuliia.ALA_LC_ALT)
    publishing_house_translit = iuliia.translate(publishing_house, schema=iuliia.ALA_LC_ALT)  # Транслитерированное издательство
    # Перевод названия
    try:
        translator = Translator(to_lang="en", from_lang="ru")  # Создание объекта для переводчика
        title_translated = translator.translate(title)  # Перевод названия
        if title_translated[0].isupper() is False:  # Чтобы перевод был всегда с большой буквы
            title_translated = title_translated[0].upper() + title_translated[1:]
    except:
        print("\nОтсутствует подключение к сети Интернет. Перевод на английский язык невозможен.\n")
    if title_translated.find("MYMEMORY WARNING") != -1:
        hours = title_translated[title_translated.find("HOURS") - 3: title_translated.find("HOURS")].strip()
        title_translated = title_translated[title_translated.find("HOURS"):]
        minutes = title_translated[title_translated.find("MINUTES") - 3: title_translated.find("MINUTES")].strip()
        if hours[0] == "0":
            hours = hours[1:]
        if minutes[0] == "0":
            minutes = minutes[1:]

        if int(hours) == 0:
            hours_word = ""
            hours = ""
        elif int(hours) == 1:
            hours_word = "час"
        elif int(hours) <= 4 and int(hours) != 1:
            hours_word = "часа"
        else:
            hours_word = "часов"
        
        if int(minutes) == 0:
            minutes_word = ""
            minutes = ""
        elif int(minutes) == 1:
            minutes_word = "минуту"
        elif int(minutes) <= 4 and int(minutes) != 1:
            minutes_word = "минуты"
        else:
            minutes_word = "минут"
        print(f"\nЛимит переводов исчерпан. Данная проблема связана с политикой корпорации \"Google\". Попробуйте снова через {hours} {hours_word} {minutes} {minutes_word}.\n")
        title_translated = ""
    # Создание новой строки для reference
    string_making = Authors_conversion(authors_arr_translit, editors_arr_translit)  # См. в String_convertion.py
    new_reference = string_making[0]
    editors_arr_translit = string_making[1]
# Проверка к какому типу издания относится публикация
    return_string_for_batch = ""
    if name_of_compilation_or_journal_translit == "":
        return_string_for_batch = Monografy_conversion(new_reference, authors_arr_translit, editors_arr_translit, year, title_translit, title_translated, city_translit, publishing_house_translit, foliant, pages)
    elif name_of_compilation_or_journal_translit != "" and number == "":
        return_string_for_batch = Compilation_conversion(new_reference, authors_arr_translit, editors_arr_translit, year, title_translit, title_translated, name_of_compilation_or_journal_translit, city_translit, publishing_house_translit, foliant, pages)
    elif number != "" and city == "":
        return_string_for_batch = Journal_conversion(new_reference, authors_arr_translit, year, title_translit, title_translated, name_of_compilation_or_journal_translit, number, pages)
    return return_string_for_batch
