from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SeleniumExceptions
from bs4 import BeautifulSoup
import os
import time
import scraper.constants as const
from selenium.webdriver.chrome.options import Options


class SchoolScraper(webdriver.Chrome):
    ids = []
    names = []
    credits = []
    tags = []
    subjects = []
    terms = []
    eligible_grades = []
    prerequisites = []
    corequisites = []
    elective = []
    schools = []

    data_values = []

    def __init__(self, driver_path=r"E:\Selenium", teardown=False, expand_initially=False, debug=True, options=None):
        self.driver_path = driver_path
        self.teardown = teardown
        self.debug = debug
        os.environ['PATH'] += ";" + self.driver_path
        super(SchoolScraper, self).__init__(options=options)
        self.expand = False
        if expand_initially:
            self.show_all_courses()

        if options is None:
            self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    # executes all the things that are required for it to run everything
    def run(self):
        self.land_page()
        print("LOADED PAGE")
        self.set_base_data()
        print("LOADED ALL COURSES")
        self.show_all_courses()  # unshows the courses, makes the page load lot faster
        self.set_school_data()
        print("LOADED ALL SCHOOLS")

    def land_page(self):
        self.get(const.URL)

    def show_all_courses(self):
        # waits until show all courses is clickable
        try:
            WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'css-r5v11l'))
            )
            self.find_element(By.CLASS_NAME, 'css-r5v11l').click()
        except SeleniumExceptions.ElementClickInterceptedException:
            pass
        self.expand = True

    def set_school_data(self):

        for i in range(len(self.ids)):
            self.schools.append("")

        # finds the number of schools that need to be checked
        WebDriverWait(self, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'U76MQ'))
        )
        self.find_element(By.CLASS_NAME, 'U76MQ').click()

        WebDriverWait(self, 30).until(
            EC.element_to_be_clickable((
                By.CLASS_NAME, 'T3JZ2'))
        )

        WebDriverWait(self.find_element(
            By.CLASS_NAME, 'T3JZ2'), 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'Lk3AP'))
        )

        self.find_element(
            By.CLASS_NAME, 'T3JZ2').find_elements(
            By.CLASS_NAME, 'Lk3AP')[1].click()

        school_count = len(self.find_element(
            By.CSS_SELECTOR, 'div[role="presentation"]').find_elements(
            By.CSS_SELECTOR, 'div[role="button"]')
        )

        if self.debug:
            school_count = const.SCHOOL_COUNT

        # calls select school and get table html and then adds this school to the list of schools that offer that course
        # does the above for all schools
        for i in range(school_count):

            # deselect old school and select only one school
            if i - 1 >= 0:
                self.select_school(i - 1)
            school_name = self.select_school(i)

            if school_name.__contains__('COMPLETED' or 'Elementary'):
                break
            # read the html data of the school
            html_table = self.get_table_html()
            if len(html_table) != 1:
                for x in range(len(html_table)):
                    row_elements = BeautifulSoup(html_table[x].get_attribute('innerHTML'), 'lxml').find_all('td')
                    if self.ids.__contains__(self.get_ids(row_elements)):
                        self.schools[self.ids.index(self.get_ids(row_elements))] += school_name + ","
                print(school_name, 'PROCESSED')
        for i in range(len(self.schools)):
            self.schools[i] = self.schools[i][0:len(self.schools[i]) - 1]
            if self.schools[i] is None:
                self.schools[i] = ""

    def select_school(self, school_number):

        # clicks on school_number school in the list on the site and selects it

        # if the filter is not already selected then select it
        try:
            WebDriverWait(self, 15).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'U76MQ'))
            )
            self.find_element(By.CLASS_NAME, 'U76MQ').click()
            return "COMPLETED"
        # if it is then pass the exception to it already being selected
        except SeleniumExceptions.ElementClickInterceptedException:
            pass

        WebDriverWait(self, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'T3JZ2'))
        )
        WebDriverWait(self.find_element(By.CLASS_NAME, 'T3JZ2'), 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Lk3AP'))
        )
        self.find_element(By.CLASS_NAME, 'T3JZ2').find_elements(
            By.CLASS_NAME, 'Lk3AP')[1].click()

        name = self.find_element(By.CSS_SELECTOR, 'div[role="presentation"]').find_elements(
            By.CSS_SELECTOR, 'div[role="button"]')[school_number].text

        WebDriverWait(self.find_element(By.CSS_SELECTOR, 'div[role="presentation"]'), 15).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'div[role="button"]'))
        )
        self.find_element(By.CSS_SELECTOR, 'div[role="presentation"]').find_elements(
            By.CSS_SELECTOR, 'div[role="button"]')[school_number].click()

        return name

    def get_table_html(self):
        # waits until table is findable
        WebDriverWait(self, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-r5v11l'))
        )

        # waits until table has actual data
        try:
            WebDriverWait(
                self.find_element(By.CSS_SELECTOR, 'table[aria-labelledby="tableTitle"]')
                .find_element(By.TAG_NAME, 'tbody')
                .find_element(By.TAG_NAME, 'tr'), 10
            ).until_not(
                EC.text_to_be_present_in_element((By.TAG_NAME, 'td'), 'No courses found.')
            )
        except SeleniumExceptions.TimeoutException:
            return self.find_element(
                By.CSS_SELECTOR, 'table[aria-labelledby="tableTitle"]').find_element(
                By.TAG_NAME, 'tbody').find_elements(
                By.TAG_NAME, 'tr'
            )

        # reads data from body of table
        body = self.find_element(By.CSS_SELECTOR, 'table[aria-labelledby="tableTitle"]').find_element(By.TAG_NAME, 'tbody')

        i = 0
        # loops until all courses are in the table
        while True:
            # presses end to move the table down
            actions = ActionChains(self)
            actions.move_to_element(body).perform()
            actions.send_keys(Keys.END).perform()
            try:
                wait = WebDriverWait(self, const.LOADTIME, .1)
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[viewBox="22 22 44 44"]'))
                )
            except SeleniumExceptions.TimeoutException:
                break
            # checks if the table has started to load new things

            # runs only the amount of courses wanted for debbuging purposes (tests with a smaller number of courses
            # runs only the amount of courses wanted for debbuging purposes (tests with a smaller number of courses
            if self.debug and i >= const.COURSE_COUNT:
                print("ENDED WITH DEBUG COUNTER")
                break
            elif self.debug:
                i = len(self.find_element(
                    By.CSS_SELECTOR, 'table[aria-labelledby="tableTitle"]').find_element(
                    By.TAG_NAME, 'tbody').find_elements(
                    By.TAG_NAME, 'tr')
                )

            # if so then wait till the stuff is loaded

        # expands table if not expanded already
        if not self.expand:
            self.show_all_courses()

        return body.find_elements(By.TAG_NAME, 'tr')

    def get_ids(self, row_elements):
        return row_elements[0].text

    def get_names(self, row_elements):
        return row_elements[1].text

    def get_credits(self, row_elements):
        return row_elements[2].text

    def get_tags(self, row_elements):
        tags = ''
        for i in row_elements[3].find_all('div'):
            if not tags.__contains__(i.text):
                tags += i.text + ','
        return tags[0:len(tags) - 1]

    def get_subjects(self, row_elements):
        return row_elements[0].div.div.find_all('div')[0].text.replace('Subject:  ', '').replace('\n', '')

    def get_terms(self, row_elements):
        return row_elements[0].div.div.find_all('div')[1].text.replace('Term:  ', '').replace('\n', '')

    def get_elegible_grades(self, row_elements):
        return row_elements[0].div.div.find_all('div')[2].text.replace('Eligible Grades:  ', '').replace('\n', '')

    def get_prerequisites(self, row_elements):
        return row_elements[0].div.div.find_all('div')[3].text.replace('Prerequisite:  ', '').replace('\n', '')

    def get_corequisites(self, row_elements):
        return row_elements[0].div.div.find_all('div')[4].text.replace('Corequisite:  ', '').replace('\n', '')

    def get_elective(self, row_elements):
        return row_elements[0].div.find('div', class_='MtzHK').text is not None

    def set_base_data(self):

        # gets all the rows of the table and splits them into the header rows and the expanded rows
        html_table = self.get_table_html()
        header_rows = [n for index, n in enumerate(html_table) if not index % 2]
        expanded_rows = [n for index, n in enumerate(html_table) if index % 2]

        # iterates over all the courses (every two rows is a course because of expansion)
        for i in range(int(len(html_table) / 2)):

            # sets rows for the basic course data
            row = header_rows[i].get_attribute('innerHTML')
            row_elements = BeautifulSoup(row, 'lxml').find_all('td')
            self.ids.append(self.get_ids(row_elements))
            self.names.append(self.get_names(row_elements))
            self.credits.append(self.get_credits(row_elements))
            self.tags.append(self.get_tags(row_elements))

            # sets rows for the expanded row data
            row = expanded_rows[i].get_attribute('innerHTML')
            row_elements = BeautifulSoup(row, 'lxml').find_all('td')
            self.subjects.append(self.get_subjects(row_elements))
            self.terms.append(self.get_terms(row_elements))
            self.eligible_grades.append(self.get_elegible_grades(row_elements))
            self.prerequisites.append(self.get_prerequisites(row_elements))
            self.corequisites.append(self.get_corequisites(row_elements))
            self.elective.append(self.get_elective(row_elements))

        self.data_values = [
            self.ids,
            self.names,
            self.credits,
            self.tags,
            self.subjects,
            self.terms,
            self.eligible_grades,
            self.prerequisites,
            self.corequisites,
            self.elective,
            self.schools
        ]

        if self.debug:
            print(self.ids)
            print(self.names)
            print(self.credits)
            print(self.tags)
            print(self.subjects)
            print(self.terms)
            print(self.eligible_grades)
            print(self.prerequisites)
            print(self.corequisites)
            print(self.elective)
            print(self.schools)

    def get_value(self, value_type):
        return self.data_values[const.FIELDNAMES.index(value_type)]

    def course_count(self):
        return len(self.data_values[0])
