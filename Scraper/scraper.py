from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
import Scraper.constants as const


class SchoolScraper(webdriver.Chrome):

    courses_id = []
    courses_name = []
    courses_credits = []
    courses_tags = []
    courses_subject = []
    courses_term = []
    courses_eligible_grades = []
    courses_prerequisite = []
    courses_corequisite = []
    courses_elective = []

    def __init__(self, driver_path=r"E:\Selenium", teardown=False, minimize=False, expand_initially=False, debug=True):
        self.driver_path = driver_path
        self.teardown = teardown
        self.minimize = minimize
        self.expand = expand_initially
        self.debug = debug
        os.environ['PATH'] += ";" + self.driver_path
        super(SchoolScraper, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_page(self):
        self.get(const.URL)

    def show_all_courses(self):
        # waits until show all courses is clickable
        WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-r5v11l'))
        )
        self.find_element(By.CLASS_NAME, 'css-r5v11l').click()

        # minimizes if not done already
        if self.minimize:
            self.minimize_window()
            self.minimize = False

    def get_table_html(self):
        # waits until table is findable
        WebDriverWait(self, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-r5v11l'))
        )

        # minimizes if not done already


        # expands the table if wanted to be done before
        if self.expand:
            self.show_all_courses()

        # set expanded to false so that later it can be expanded under no matter what
        self.expand = False

        # waits until table has actual data
        WebDriverWait(
            self.find_element(By.CSS_SELECTOR, 'table[aria-labelledby="tableTitle"]')
            .find_element(By.TAG_NAME, 'tbody')
            .find_element(By.TAG_NAME, 'tr'), 10  # seconds
        ).until_not(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'td'), 'No courses found.')
        )

        if self.minimize:
            self.minimize_window()
            self.minimize = False
        # reads data from body of table
        body = self.find_element(By.CSS_SELECTOR, 'table[aria-labelledby="tableTitle"]').find_element(By.TAG_NAME, 'tbody')

        # loops until all courses are in the table
        while len(body.find_elements(By.TAG_NAME, 'tr')) < (const.COURSE_COUNT if not self.expand else const.COURSE_COUNT * 2):
            actions = ActionChains(self)
            actions.move_to_element(body).perform()
            actions.send_keys(Keys.END).perform()
            current_len = len(body.find_elements(By.TAG_NAME, 'tr'))

            # waits before pressing end again so that table is being told to move while loading
            while len(body.find_elements(By.TAG_NAME, 'tr')) <= current_len:
                time.sleep(.1)
                if self.debug:
                    print(len(body.find_elements(By.TAG_NAME, 'tr')), 'rechecking...')

            # recounts the number of rows to check if it has reached the end
            row_count = len(
                self.find_element(By.CSS_SELECTOR, 'table[aria-labelledby="tableTitle"]')
                .find_element(By.TAG_NAME, 'tbody')
                .find_elements(By.TAG_NAME, 'tr')
            )

            if self.debug:
                print(len(body.find_elements(By.TAG_NAME, 'tr')))

        # expands table if not expanded already
        if not self.expand:
            self.show_all_courses()

        return body.find_elements(By.TAG_NAME, 'tr')

    def get_course_id(self, row_elements):
        return row_elements[0].text

    def get_course_name(self, row_elements):
        return row_elements[1].text

    def get_course_credit(self, row_elements):
        return row_elements[2].text

    def get_course_tags(self, row_elements):
        tags = ''
        for i in row_elements[3].find_all('div'):
            if not tags.__contains__(i.text):
                tags += i.text + ','
        return tags[0:len(tags) - 1]

    def get_course_subject(self, row_elements):
        return row_elements[0].div.div.find_all('div')[0].text.replace('Subject:  ', '')

    def get_course_term(self, row_elements):
        return row_elements[0].div.div.find_all('div')[1].text.replace('Term:  ', '')

    def get_course_elegible_grades(self, row_elements):
        return row_elements[0].div.div.find_all('div')[2].text.replace('Eligible Grades:  ', '')

    def get_course_prerequisite(self, row_elements):
        return row_elements[0].div.div.find_all('div')[3].text.replace('Prerequisite:  ', '')

    def get_course_corequisite(self, row_elements):
        return row_elements[0].div.div.find_all('div')[4].text.replace('Corequisite:  ', '')

    def get_course_elective(self, row_elements):
        return row_elements[0].div.find('div', class_='MtzHK').text != ''

    def set_all_data(self):

        # gets all the rows of the table and splits them into the header rows and the expanded rows
        html_table = self.get_table_html()
        header_rows = [n for index, n in enumerate(html_table) if not index % 2]
        expanded_rows = [n for index, n in enumerate(html_table) if index % 2]

        # iterates over all the courses (every two rows is a course because of expansion)
        for i in range(int(len(html_table) / 2)):
            # sets rows for the basic course data
            row = header_rows[i].get_attribute('innerHTML')
            row_elements = BeautifulSoup(row, 'lxml').find_all('td')
            self.courses_id.append(self.get_course_id(row_elements))
            self.courses_name.append(self.get_course_name(row_elements))
            self.courses_credits.append(self.get_course_credit(row_elements))
            self.courses_tags.append(self.get_course_tags(row_elements))

            # sets rows for the expanded row data
            row = expanded_rows[i].get_attribute('innerHTML')
            row_elements = BeautifulSoup(row, 'lxml').find_all('td')
            self.courses_subject.append(self.get_course_subject(row_elements))
            self.courses_term.append(self.get_course_term(row_elements))
            self.courses_eligible_grades.append(self.get_course_elegible_grades(row_elements))
            self.courses_prerequisite.append(self.get_course_prerequisite(row_elements))
            self.courses_corequisite.append(self.get_course_corequisite(row_elements))
            self.courses_elective.append(self.get_course_elective(row_elements))

        if self.debug:
            print(self.courses_id)
            print(self.courses_name)
            print(self.courses_credits)
            print(self.courses_tags)
            print(self.courses_subject)
            print(self.courses_term)
            print(self.courses_eligible_grades)
            print(self.courses_prerequisite)
            print(self.courses_corequisite)
            print(self.courses_elective)

