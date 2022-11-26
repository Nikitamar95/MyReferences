# -*- coding: utf-8 -*-
#
#  Functions_for_string.py
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
from Service_arrays import cleargy_arr, cleargy_dict


# Функции для работы со строкой
# Поиск авторов
# Если несколько авторов. Создаётся список авторов
def Find_Authors(func_string):
    authors_arr_func = []
    # Описываются разнообразные условия
    # Если до ". " есть цифры, т.е. год.
    point_space_position = func_string.find(". ")
    digit = 0
    for i in range(0, point_space_position):
        if func_string[i].isdigit() is True:
            digit = 1
            break
    # Проверка не является ли последний автор клириком
    last_author_is_cleric = 0
    last_comma = func_string[: point_space_position].rfind(", ")
    if last_comma != -1:
        for i in cleargy_arr:
            if func_string[last_comma + 1: point_space_position + 1].find(i) != -1:
                last_author_is_cleric = 1
        for i in cleargy_dict.keys():
            if func_string[last_comma + 1: point_space_position + 1].find(i) != -1:
                last_author_is_cleric = 1
    # Поиск инициалов, ели есть "/" или год, тогда авторов нет.
    if digit != 1 and func_string.find("/", 0, point_space_position) == -1 and (func_string[point_space_position-1].isupper() is True or last_author_is_cleric == 1):
        authors = func_string[:func_string.find(". ")+1].strip()  # Поиск авторов и создание их списка
        while authors.find(",") != -1:
            authors_arr_func.append(authors[:authors.find(",")].strip())
            authors = authors[authors.find(",")+1:].strip()
        authors_arr_func.append(authors.strip())
        func_string = func_string[func_string.find(". ")+1:].strip()
    return func_string, authors_arr_func


# Поиск названия публикации
def Find_Title(func_string):
    if func_string.find("/") != -1:
        title_func = func_string[:func_string.find("/")].strip()
        func_string = func_string[func_string.find("/"):].strip()
    else:
        title_func = func_string[:func_string.find(". ")].strip()
        func_string = func_string[func_string.find(". ")+1:].strip()
    return func_string, title_func
# Поиск названия книги/журнала


def Find_name_of_compilation_or_journal(func_string):
    name_of_compilation_or_journal_func = ""
    if func_string[0] == "/" and func_string[1] != "/":
        pass
    elif func_string[0] == "/" and func_string[1] == "/":
        func_string = func_string[2:].strip()
        if func_string.find("/") != -1:
            name_of_compilation_or_journal_func = func_string[:func_string.find("/")].strip()
            func_string = func_string[func_string.find("/"):].strip()
        else:
            name_of_compilation_or_journal_func = func_string[:func_string.find(". ")]
            func_string = func_string[func_string.find(". ")+2:]
    return func_string, name_of_compilation_or_journal_func


def Find_Editors(func_string):
    editors_arr_func = []
    if func_string[0] == "/":
        func_string == func_string[1:]
        for i in range(len(func_string)):
            if func_string[i] == "." and func_string[i-1].isupper() is True:  # Поиск места, где заканчиваются слова "под редакцией"
                func_string = func_string[i-1:].strip()                    # и начинаются инициалы
                break
        for i in range(1, len(func_string)):
            if func_string[i] == "." and func_string[i-1].islower() is True:  # Поиск конца перечисления редакторов
                editors = func_string[:i].strip()
                break
        func_string = func_string[len(editors)+1:].strip()
        while editors.find(",") != -1:  # Разъединение редакторов и создание списка их имён
            editors_arr_func.append(editors[:editors.find(",")+1].rstrip(",").strip())
            editors = editors[editors.find(",")+1:].strip()
        editors_arr_func.append(editors)
    return func_string, editors_arr_func


def Find_city_and_publishing_house(func_string):
    publishing_house_func = ""
    city_func = ""
    if func_string[0].isdigit() is False:
        if func_string.find(":") == -1:
            city_func = func_string[:func_string.find(",")+1].rstrip(",")  # Город, если нет издательства
        else:
            city_func = func_string[:func_string.find(":")]  # Город, если есть издательство
            publishing_house_func = func_string[func_string.find(":")+1:func_string.find(",")].strip()
        func_string = func_string[func_string.find(",")+1:].strip()
    return func_string, city_func, publishing_house_func


def Find_a_year(func_string):
    year_func = func_string[:func_string.find(".")+1].rstrip(".")
    func_string = func_string[func_string.find(".")+1:].strip()
    return func_string, year_func


def Find_a_numder(func_string):
    number_func = ""
    if func_string.find("№") != -1:
        number_func = func_string[func_string.find("№")+1: func_string.find(".")].strip()
        func_string = func_string[func_string.find(".")+1:].strip()
    return func_string, number_func


def Find_a_foliant(func_string):
    foliant_func = ""
    if func_string.find("Т.") != -1 or func_string.find("Вып.") != -1:
        func_string = func_string[func_string.find(".")+1:].strip()
        foliant_func = func_string[:func_string.find(".")].strip()
        func_string = func_string[func_string.find(".")+1:].strip()
    return func_string, foliant_func


def Find_pages(func_string):
    pages_func = ""
    if func_string.find("С.") != -1:
        func_string = func_string[func_string.find("С.")+2:].strip()
        pages_func = func_string[:func_string.find(".")].strip()
    elif func_string.find("с.") != -1:
        pages_func = func_string[:func_string.find("с.")].strip()
    return pages_func
