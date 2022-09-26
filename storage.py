import csv
from reading.course import Course
courses = []
with open ("classes.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        credits = (float)(row["credits"])
        tags = row["tags"].split(",")
        grades = row["grades"].split(",")
        prereqs = row["prerequisites"].split(",")
        coreqs = row["corequisites"].split(",")
        schools = row["schools"].split(",")
        gpa = 4
        if "AP" in tags or "KAP" in tags:
            gpa = 5
        elif "Dual Credit" in tags:
            gpa = 4.5
        courses.append(Course(id=row["id"], name=row["name"], credits=credits, tags=tags, subject=row["subject"], term=row["term"], grades=grades, prerequisites=prereqs, corequisites=coreqs, schools=schools, gpa=gpa))
        # make sure corequisites also work as prerequisites when making schedule