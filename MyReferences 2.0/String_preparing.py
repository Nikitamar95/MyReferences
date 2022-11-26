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

import QuaestioRossica
from Functions_for_string import *
from Service_arrays import cleargy_arr, cleargy_dict


# Библиотека для транслитерации https://pypi.org/project/iuliia/
import iuliia
# Библиотека для перевода https://pypi.org/project/translate/
from translate import Translator

internet_warning_is_shown = False
internet_warning_text = ""
google_warning_is_shown = False
google_warning_text = ""


def Batch_process():
    file_with_russian_references = open("Ref_Rus.txt", 'r+')
    file_with_english_references = open("Ref_Eng.txt", 'w+')
    read_string = file_with_russian_references.readline().strip()
    num = 1
    while read_string != "":
        # Если перед строкой есть номера, например: 1) или 1.
        if read_string[0].isdigit() is True and read_string.find(")") != -1:
            read_string = read_string[read_string.find(")")+1:].strip()
        elif read_string[0].isdigit() is True and read_string[read_string.find(".")-1].isdigit() is True:
            read_string = read_string[read_string.find(".")+1:].strip()
        try:
            append_to_new_file = String_preparing(read_string)
        except:
            file_with_english_references.write('Строка № ' + str(num) + ' не может быть обработана' + '\n')
        else:
            if append_to_new_file != "":
                # Вариант с нумерацией
                # file_with_english_references.write(str(num) + '. ' + append_to_new_file + '\n')
                file_with_english_references.write(append_to_new_file + '\n')
            else:
                file_with_english_references.write('Строка № ' + str(num) + ' не может быть обработана' + '\n')
        num += 1
        read_string = file_with_russian_references.readline().strip()
    file_with_russian_references.close()
    file_with_english_references.close()

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
        global internet_warning_is_shown, internet_warning_text
        if internet_warning_is_shown is False:
            internet_warning_text = "Отсутствует подключение к сети Интернет. Перевод на английский язык невозможен."
            internet_warning_is_shown = True
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
        global google_warning_is_shown, google_warning_text
        if google_warning_is_shown is False:
            google_warning_text = f"Лимит переводов исчерпан. Данная проблема связана с политикой корпорации \"Google\". Попробуйте снова через {hours} {hours_word} {minutes} {minutes_word}."
            google_warning_is_shown = True
        title_translated = ""
    """
    Здесь надо вставить проверку модуля
    """

    # Создание новой строки для reference
    string_making = QuaestioRossica.Authors_conversion(authors_arr_translit, editors_arr_translit)  # См. в String_convertion.py
    new_reference = string_making[0]
    #print(new_reference, authors_arr_translit)
    editors_arr_translit = string_making[1]
# Проверка к какому типу издания относится публикация
    return_string_for_batch = ""
    if name_of_compilation_or_journal_translit == "":
        return_string_for_batch = QuaestioRossica.Monografy_conversion(new_reference, authors_arr_translit, editors_arr_translit, year, title_translit, title_translated, city_translit, publishing_house_translit, foliant, pages)
    elif name_of_compilation_or_journal_translit != "" and number == "":
        return_string_for_batch = QuaestioRossica.Compilation_conversion(new_reference, authors_arr_translit, editors_arr_translit, year, title_translit, title_translated, name_of_compilation_or_journal_translit, city_translit, publishing_house_translit, foliant, pages)
    elif number != "" and city == "":
        return_string_for_batch = QuaestioRossica.Journal_conversion(new_reference, authors_arr_translit, year, title_translit, title_translated, name_of_compilation_or_journal_translit, number, pages)
    return return_string_for_batch
