import csv
from reading.course import Course
import scraper.constants as const


class Storage:
    courses = []

    def __init__(self, school):
        with open(const.FILE_NAME) as file:
            reader = csv.DictReader(file)
            for row in reader:
                # checking if the course has already been added

                name = row['name'][:-1]
                # removing the course identifiers and tags from them because they are also shown in the tags
                if 'KAP/GT ' in name:
                    name.replace('KAP/GT ', '')
                if 'KAP ' in name:
                    name.replace('KAP ', '')
                if 'AP ' in name:
                    name.replace('AP ', '')
                if 'KVS ' in name:
                    name.replace('KVS ', '')

                credit = float(row['credits'])
                tags = row['tags'].split(',')
                grades = row['eligible_grades'].split(',')
                prereqs = row['prerequisite'].split(',')
                coreqs = row['corequisite'].split(',')
                schools = row['schools'].split(',')
                gpa = 4
                if 'AP' in tags or 'KAP' in tags:
                    gpa = 5
                elif 'DC' in tags:
                    gpa = 4.5
                course = Course(row['id'], name, credit, tags, row['subject'], row['term'], grades, prereqs, coreqs, schools, gpa, row['elective'])
                valid = True
                for val in self.courses:
                    if course == val:
                        valid = False
                        break
                if valid and school in course.schools:
                    self.courses.append(course)
                # make sure corequisites also work as prerequisites when making schedule
            for course in self.courses:
                print(course)
