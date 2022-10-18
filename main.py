from typing import Dict
from reading.storage import get_by_name

from writer.writer import Writer


if input('Should we scrape? ').__contains__('y' or 'Y'):
    writer = Writer()
    writer.get_data()
    writer.write()

# import reader and do the reading here

# basic info
school = input('What school do you go to? ')
major = input('What do you want to major in? ')

# interest in fields of study
print('On a Scale of 1 - 10 describe the following:')
interest = {}
interest['CS'] = int(input('Interest in Computer Science? '))
interest['Business'] = int(input('Interest in Business? '))
interest['Public Speaking/Writing'] = int(input('Interest in Public Speaking/Writing? '))
interest['Engineering'] = int(input('Interest in Engineering? '))
interest['Medical'] = int(input('Interest in the Medical Field? '))
interest['History'] = int(input('Interest in History? '))

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

# middle school
print('On the following courses, state if taken in middle school: ')
taken = {}
lang = input('What foreign language? ') if input('A foreign language? ').__contains__('y' or 'Y') else ""
taken['Language'] = lang
math = 'Geometry' if input('Geometry? ').__contains__('y' or 'Y') else 'Algebra 1' if input('Algebra 1? ').__contains__('y' or 'Y') else ""
taken['Math'] = math

ninth = []
ninth.append(get_by_name('AP Human Geography A'))
ninth.append(get_by_name('AP Computer Science Principles A'))
ninth.append(get_by_name('Biology KAP A'))
ninth.append(get_by_name('AP Human Geography A'))
ninth.append(get_by_name('Orchestra 1A'))
ninth.append(get_by_name('Spanish 1A'))
ninth.append(get_by_name('Geometry KAP/GT A'))

for course in ninth:
    print(
        f'ID: {course.id}, Name:{course.name}, Credits:{course.credits}, Subject:{course.subject}, Tags: {course.tags}')


