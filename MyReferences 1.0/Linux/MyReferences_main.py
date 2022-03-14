#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MyReferences_main.py
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

from About_the_program import About
from String_preparing import String_preparing
from Batch_process import Batch_process
from Service_arrays import exit_array, about_array, batch_arr
from Info import Info

# Первоначальный вызов шапки
Info()


def Main_function():
    main_string = ""
    while main_string not in exit_array:
        print("Введите исходный текст элемента библиографического списка и нажмите клавишу \"Enter\"\n      Важно! Использование пробелов между инициалами НЕ ДОПУСКАЕТСЯ\n")
        main_string = input()
        if main_string in exit_array:  # Обработка выхода в систему и информации о программе
            raise SystemExit()
        elif main_string in about_array:
            About()
            Info()
            launching_the_program()
        elif main_string in batch_arr:
            Batch_process()
            launching_the_program()
        String_preparing(main_string)
    else:
        raise SystemExit()


# Главная функция вызывающая программу
def launching_the_program():
    try:
        Main_function()
    except SystemExit:
        raise SystemExit()
    except:
        print("")
        print("К сожалению, введённые Вами данные не могут быть корректно обработаны.\nПостарайтесь уточнить или упростить синтаксис вводимого элемента библиографического списка.\nДля просмотра раздела справки введите \"о\" и нажмите клавишу \"Enter\"\n")
        launching_the_program()


# Вызов главной функции
launching_the_program()
