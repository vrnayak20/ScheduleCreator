class Course:
    def __init__(self, id, name, credits, tags,subject,term,grades,prerequisites,corequisites,schools, gpa):
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
