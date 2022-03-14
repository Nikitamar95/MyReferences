#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  About_the_program.py
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

from Clear_screen import clear
from Service_arrays import exit_array, license_array


def About():
    clear()
    instruction_file = open("About_the_program.txt")
    instruction_txt = instruction_file.read()
    print(instruction_txt)
    instruction_file.close()
    print("Для выхода из раздела справки введите \"в\" \
и нажмите клавишу \"Enter\"")
    print("Для просмотра лицензии введите \"л\" и нажмите клавишу \"Enter\"")
    menu_input = ""
    while menu_input not in exit_array and menu_input not in license_array:
        menu_input = input()
    if menu_input in exit_array:
        clear()
    else:
        menu_input = ""
        clear()
        license_file = open("License.txt")
        license_txt = license_file.read()
        license_file.close()
        print(license_txt)
        print("Для выхода в главное меню введите \"в\" \
и нажмите клавишу \"Enter\"")
        while menu_input not in exit_array:
            menu_input = input()
        if menu_input in exit_array:
            clear()
