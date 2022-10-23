from typing import Dict
from reading.storage import Storage
from writer.writer import Writer


if input('Should we scrape? ').__contains__('y' or 'Y'):
    writer = Writer()
    writer.get_data()
    writer.write()

# import reader and do the reading here
storing = Storage()

# basic info
school = input('What school do you go to? ')

# interest in fields of study
print('On a Scale of 1 - 10 describe the following:')
interest = {'CS': int(input('Interest in Computer Science? ')), 'Business': int(input('Interest in Business? ')),
            'Public Speaking/Writing': int(input('Interest in Public Speaking/Writing? ')),
            'Engineering': int(input('Interest in Engineering? ')),
            'Medical': int(input('Interest in the Medical Field? ')), 'History': int(input('Interest in History? '))}

# middle school
print('On the following courses, state if taken in middle school: ')
taken = {}
lang = input('What foreign language? ') if input('A foreign language? ').__contains__('y' or 'Y') else ""
taken['Language'] = lang
math = 'Geometry' if input('Geometry? ').__contains__('y' or 'Y') else 'Algebra' if input('Algebra 1? ').__contains__('y' or 'Y') else ""
taken['Math'] = math

# other intersts
fine_arts = input('What fine arts did you take in Middle school')
interest['Fine Arts'] = int(input(f'Interest in {fine_arts}? '))
interest['GPA'] = int(input('Interest in GPA? '))
interest['Fun'] = int(input('Interest in taking fun courses? '))
interest['History'] = int(input('Interest in History? '))
interest['5.0 over Nothing'] = int(input('On a Scale of 1 - 10 if you had the option to take a course that you '
                                         'preferred (5.0) or not take any course at all (Not Counted), '
                                         'how much would you want to take the course? '))

interest['4.0 over Nothing'] = int(input('On a Scale of 1 - 10 if you had the option to take a course that you '
                                         'preferred (4.0) or not take any course at all (Not Counted), how much '
                                         'would you want to take the course still? '))
interest['AP'] = int(input('On a Scale of 1 - 10 how much do you value AP courses (Harder but provide college credit)'))
interest['Easy'] = int(input('On a Scale of 1 - 10 how much would want to take a course you do not like but is easy? '))
