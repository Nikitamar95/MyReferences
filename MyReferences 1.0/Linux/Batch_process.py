# -*- coding: utf-8 -*-
#
#  Batch_process.py
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

from String_preparing import String_preparing
from Clear_screen import clear
from Info import Info


def Batch_process():
    try:
        file_with_russian_references = open("Ref.txt")
    except:
        print("\nПоместите в папку с программой файл \"Ref.txt\" и повторите попытку\n")
    else:
        file_with_english_references = open("Ref_Eng.txt", 'w')
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
        clear()
        Info()
