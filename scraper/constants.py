from selenium.webdriver.chrome.options import Options


OPTIONS = Options()
URL = r"https://app.schoolinks.com/course-catalog/katy-isd/course-offerings"
COURSE_COUNT = 1275
FILE_NAME = 'courses.csv'

FIELDNAMES = [
    'courses_id',
    'courses_name',
    'courses_credits',
    'courses_tags',
    'courses_subject',
    'courses_term',
    'courses_eligible_grades',
    'courses_prerequisite',
    'courses_corequisite',
    'courses_elective']


def HEADLESS():
    OPTIONS.add_argument('--headless')
    return OPTIONS


# set home in pyvenv.cfg = E:\Python\Python310