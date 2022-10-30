from typing import Dict
from reading.storage import Storage
from writer.writer import Writer
from analyser import Schedule

if input('Should we scrape? ').__contains__('y' or 'Y'):
    writer = Writer()
    writer.get_data()
    writer.write()

# basic info
school = input('What school do you go to? ')

# interest in fields of study
print('On a Scale of 1 - 10 describe the following:')
interest = {'CS': int(input('Interest in Computer Science? ')),
            'Public Speaking': int(input('Interest in Public Speaking? ')),
            'Engineering': int(input('Interest in Engineering? ')),
            'Medical': int(input('Interest in the Medical Field? ')),
            'History': int(input('Interest in History? ')),
            'Math': int(input('Interest in Math? ')),
            'Language': int(input('Interest in Foreign Languages? ')),
            'English': int(input('Interest in English? ')),
            'GPA': {},
            'OCPE': int(input('Interest in Off Campus PE? '))}

print('For the following, do you have interest in GPA in these subject (yes or no): ')
interest['GPA']['Math'] = 'AP' if input('Math? ').__contains__(('y' or 'Y')) else ''
interest['GPA']['English'] = 'AP' if input('English? ').__contains__(('y' or 'Y')) else ''
interest['GPA']['History'] = 'AP' if input('History? ').__contains__(('y' or 'Y')) else ''
interest['GPA']['Science'] = 'AP' if input('Science? ').__contains__(('y' or 'Y')) else ''
interest['GPA']['Elective'] = 'AP' if input('Elective? ').__contains__(('y' or 'Y')) else ''

fine_arts = input('What is your favorite fine arts?')
interest['Fine Arts'] = int(input(f'Interest in {fine_arts}? '))
# middle school
print('On the following courses, state if taken in middle school: ')
taken = {}
lang = input('What foreign language? ') if input('A foreign language? ').__contains__('y' or 'Y') else ""
taken['Language'] = lang
math = 'Geometry' if input('Geometry? ').__contains__('y' or 'Y') else 'Algebra' if input('Algebra 1? ').__contains__('y' or 'Y') else ""
taken['Math'] = math

analyser = Schedule(school, interest, taken, fine_arts)
analyser.print_schedule()


# other intersts
