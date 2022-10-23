class Course:
    def __init__(self, id, name, credits, tags,subject,term,grades,prerequisites,corequisites,schools, gpa, fun):
        self.id = id
        self.name = name
        self.credits = credits
        self.tags = tags
        self.subject = subject
        self.term = term
        self.grades = grades
        self.prerequisites = prerequisites
        self.corequisites = corequisites
        self.schools = schools
        self.gpa = gpa
        self.fun = fun

    def __str__(self):
        return f'ID: {self.id}, ' \
               f'Name: {self.name}, ' \
               f'Subject: {self.subject}, ' \
               f'Tags: {self.tags}, ' \
               f'GPA: {self.gpa}, ' \
               f'Credits: {self.credits}, ' \
               f'Grades Offered In: {self.grades}, ' \
               f'Pre-reqs: {self.prerequisites}'

    def __eq__(self, other):
        return self.name == other.name
