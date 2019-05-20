#!/usr/bin/python3

import emoji
import sys
import re

from convert_prg.teacher_list import teacher_list
from convert_prg.convert_rows import body

class header():
    """ 
    IMPORT FROM A PACKAGE
    1. create directory with package name
    2. in this directory create a __init__.py (leave it empty)
    3. create a new file and then a class with the def to import
    4. in file outside the created directory write: 
    from PACKAGENAME.FILEWITHCLASS import NAMEOFDEF 
    """

    def convert_header(rows=None, fout=None):
        
        awkward_symbols = (' ', '[', ']', '{', '}', '^', '´', '`', '°')
        def sort_class_names(represen_classes=None):
            """Return a list of the unsorted class names."""
            

            if represen_classes is None:
                print("No classes to sort given.")
                return None

            classes = []
            
            for class_name in represen_classes:

                level = re.search('\d+', class_name)
                if not level:
                    continue

                level = int(level.group())

                letter = re.findall(r'[a-d]', class_name)
                # import IPython;IPython.embed()

                # len() gets the number of items in an list e.g. l=['hi', 'bye', 'ok']
                # than len(l) is 3

                if len(letter) > 1:
                    for i in letter:
                        classes.append((level, i))
                else:
                    classes.append((level, "".join(letter)))
                
                if not letter:
                    letter = ''

                # append only takes one argument, level and letter have to be linked together
                # that is why there are two brackets: output: e.g. [(10, 'a'), ('6', 'a'), ('9', 'd')]

            return ["{}{}".format(e[0], e[1]) for e in sorted(classes)]

        def check_if_empty(check_strg=None):
            """Checks if there is anything after a : . In this case checks if a.e. 
            there are any classes missing"""
            if check_strg == None:
                print("No string to check given.")
            
            seperator = (check_strg.lower().find(':') +1 )
            second_part = check_strg.replace(check_strg[:seperator], '').replace('\xa0', '').replace('\n', '')
            second_part1 = second_part.replace(check_strg[:seperator], '').replace('\xa0', '').replace(' ', '').replace('\n', '')

            if re.match('[A-Za-z0-9]' , second_part1):
                check_strg = "".join([
                        check_strg[:seperator],
                        second_part
                    ])
            else:
                check_strg = None
    
            return check_strg

        if not rows:
            print("No rows to convert provided.")
            sys.exit(1)

        if not fout:
            print("No output file provided.")
            sys.exit(1)

        row = rows.pop(0)
        paragraphs = row.findAll('p')

        header_date = paragraphs[0]
        header_date = header_date.string.replace('\n', '')

        days = {
            'montag': 'Mo',
            'dienstag': 'Di',
            'mittwoch': 'Mi',
            'donnerstag': 'Do',
            'freitag': 'Fr',
        }
            
        for day in days:
            if day in header_date.lower():
                start_char = header_date.lower().find(day)
                header_date = "".join(
                    [
                        header_date[:start_char],
                        days.get(day),
                        header_date[start_char + len(day):],
                    ]
                )
            else:
                pass

        header_date = (header_date + emoji.emojize(' :grinning_face:',
                       use_aliases=True))

        header_classes = paragraphs[1].find('span')
        header_classes = header_classes.string
        header_classes = check_if_empty(header_classes)

        header_teacher = paragraphs[2].find('span')
        header_teacher = " ".join(
            str(i).replace('\n', '').replace('<i> </i>', '').replace('\xa0', '')
            for i in header_teacher.contents)

        start_char = header_teacher.lower().find(':')
        if header_teacher[start_char-1] == ' ':
            header_teacher = "".join([
                    header_teacher[:start_char-1],
                    header_teacher[start_char:]
                ])

        for teacher in teacher_list:
            if teacher.lower() in header_teacher.lower():
                start_char = header_teacher.lower().find(teacher.lower())
                header_teacher = "".join(
                    [
                        header_teacher[:start_char],
                        teacher_list.get(teacher),
                        header_teacher[start_char + len(teacher):],
                    ]
                )
                
        else:
            pass
        header_teacher = check_if_empty(header_teacher)

        represen_classes = []


        for row in rows:
            if len(row) == 11:
                klasse = body.convert_rows(rows=row, fout=fout, get_substitute_classes=True)
                
                if klasse == None:
                    pass
                else:
                    if klasse.lower() == 'klasse':
                        pass
                    else:
                        represen_classes.append(klasse)
       
        
        if represen_classes:
            l = -1
            for c in represen_classes:
                l += 1
                for s in awkward_symbols:
                    represen_classes[l] = represen_classes[l].replace(s, '')

            represen_classes = sort_class_names(represen_classes)
            represen_classes = set(represen_classes);represen_classes = list(sorted(represen_classes))
            represen_classes = sort_class_names(represen_classes)
            represen_classes = ("Vertretung für: " + ", ".join(represen_classes))

        if header_date:
            fout.write(header_date + '\n')
        if header_classes:
            fout.write(header_classes + '\n')
        if header_teacher:
            fout.write(header_teacher + '\n\n')
        if represen_classes:
            fout.write(represen_classes + '\n')
        
        fout.write("\n-> Klasse | Fach | Vertretung durch: (Fach) | statt\n")
       