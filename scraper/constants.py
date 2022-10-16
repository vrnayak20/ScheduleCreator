from selenium.webdriver.chrome.options import Options

OPTIONS = Options()
URL = r"https://app.schoolinks.com/course-catalog/katy-isd/course-offerings"
COURSE_COUNT = 200
SCHOOL_COUNT = 5
FILE_NAME = 'courses.csv'
LOADTIME = 15

FIELDNAMES = [
    'id',
    'name',
    'credits',
    'tags',
    'subject',
    'term',
    'eligible_grades',
    'prerequisite',
    'corequisite',
    'elective',
    'schools'
]


def HEADLESS():
    OPTIONS.add_argument('--headless')
    return OPTIONS

