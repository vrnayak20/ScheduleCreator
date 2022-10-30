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
                name: str = row['name']
                if name[-1] == ('A' or 'B'):
                    name = name[:-1]
                # if 'A ' in name:
                #    name.replace('A ', '')
                ## removing the course identifiers and tags from them because they are also shown in the tags
                if 'KVS' in name:
                    continue

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
                    if val == course:
                        valid = False
                        break

                if valid and school in course.schools and 'KVS' not in tags:
                    self.courses.append(course)

    def get_by_name(self, name, level='', grade=''):
        for i in range(len(self.courses)):
            if name in self.courses[i].name and (level == '' or level in self.courses[i].name) \
                    and (grade == '' or grade in self.courses[i].grades):
                return self.courses[i]
        return None

    def get_by_id(self, id):
        for course in self.courses:
            if course.id == id:
                return course
        return None
