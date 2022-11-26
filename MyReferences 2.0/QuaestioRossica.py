# -*- coding: utf-8 -*-
#
#  String_convertion.py
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


def Authors_conversion(authors_arr_translit, editors_arr_translit):

    new_reference = ""
    # Если нет авторов, авторы и редакторы меняются местами
    # print(authors_arr_translit, editors_arr_translit)
    if authors_arr_translit == [] and editors_arr_translit != []:
        for i in range(len(editors_arr_translit)):
            editor = editors_arr_translit[i]
            editor = editor[editor.find(". ") + 1:].strip() + ", " + editor[: editor.find(". ")+1].strip()
            new_reference += editor
            if i != len(editors_arr_translit) - 1:
                new_reference += ", "
            else:
                new_reference += " "
        authors_arr_translit = []
        editors_arr_translit = []
        new_reference += "(Eds.). "
    for i in range(len(authors_arr_translit)):  # Обработка имён авторов
        name_of_author = authors_arr_translit[i].strip()
        place_for_comma = name_of_author.find(" ")  # Поиск пробела, перед которым необходима запятая
        new_reference += name_of_author[:place_for_comma] + "," + name_of_author[place_for_comma:] + ", "
        if i == len(authors_arr_translit)-1:
            new_reference = new_reference.rstrip(", ")+" "
    return new_reference, editors_arr_translit


def Monografy_conversion(new_reference, authors_arr_translit, editors_arr_translit, year, title_translit, title_translated, city_translit, publishing_house_translit, foliant, pages):
    new_reference += f"({year}). " + f"{title_translit} " + f"[{title_translated}]"
    if editors_arr_translit != []:  # Если есть редакторы
        new_reference += " / ed. by "
        for i in range(len(editors_arr_translit)):  # Фамилия и инициалы меняются местами
            editors_initials = editors_arr_translit[i].find(". ")
            editors_name = editors_arr_translit[i]
            editors_name = editors_name[editors_initials+1:].strip()+" "+editors_name[:editors_initials+1]
            new_reference += editors_name
            if i != len(editors_arr_translit)-1:
                new_reference += ", "
            else:
                new_reference += " "
    else:
        new_reference += ". "
    new_reference += f"{city_translit}, "
    if publishing_house_translit != "":  # Если присутствует/отсутствует издательство
        new_reference += f"{publishing_house_translit}. "
    else:
        new_reference = new_reference.rstrip(", ")+". "
    if foliant != "":  # Если есть том
        if foliant.find(",") != -1 or foliant.find("-") != -1 or foliant.find("—") != -1:
            new_reference += f"Vols. {foliant}. "
        else:
            new_reference += f"Vol. {foliant}. "
    new_reference += f"{pages} p."

    return new_reference


def Journal_conversion(new_reference, authors_arr_translit, year, title_translit, title_translated, name_of_compilation_or_journal_translit, number, pages):
    new_reference += f"({year}). "+f"{title_translit} "+f"[{title_translated}]. "
    new_reference += f"In {name_of_compilation_or_journal_translit}. No. {number}, pp. {pages}."

    return new_reference


def Compilation_conversion(new_reference, authors_arr_translit, editors_arr_translit, year, title_translit, title_translated, name_of_compilation_or_journal_translit, city_translit, publishing_house_translit, foliant, pages):

    new_reference += f"({year}). " + f"{title_translit} " + f"[{title_translated}]. In "
    if editors_arr_translit != []:
        for i in range(len(editors_arr_translit)):
            editors_name = editors_arr_translit[i]
            editors_initials = editors_arr_translit[i].find(". ")
            editors_name = editors_name[editors_initials+1:].strip()+", "+editors_name[:editors_initials+1].strip()
            new_reference += editors_name
            if i != len(editors_arr_translit)-1:
                new_reference += ", "
            else:
                new_reference += " "
        new_reference += "(Ed.). "
    new_reference += f"{name_of_compilation_or_journal_translit}. {city_translit}, "
    if publishing_house_translit != "":
        new_reference += f"{publishing_house_translit}, "
    if foliant != "":
        if foliant.find(",") != -1 or foliant.find("-") != -1 or foliant.find("—") != -1:
            new_reference += f"Vols. {foliant}, "
        else:
            new_reference += f"Vol. {foliant}, "
    new_reference += f"pp. {pages}."

    return new_reference
