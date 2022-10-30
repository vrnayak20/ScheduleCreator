from reading.storage import Storage


class Schedule:
    ninth = []
    tenth = []
    eleventh = []
    twelfth = []

    def __init__(self, school, interest, taken, fine_arts):
        self.storage = Storage(school)

        # FOREIGN LANGUAGE
        if taken['Language'] != '':
            self.ninth.append(self.storage.get_by_name(taken['Language']+' 2'))
        else:
            self.ninth.append(self.storage.get_by_name('Spanish 1'))
            self.tenth.append(self.storage.get_by_name('Spanish 2'))

        # MATH
        if taken['Math'] == 'Algebra':
            self.ninth.append(self.storage.get_by_name('Geometry', interest['GPA']['Math']))
            self.tenth.append(self.storage.get_by_name('Algebra 2', interest['GPA']['Math']))
            self.eleventh.append(self.storage.get_by_name('Precalculus', interest['GPA']['Math']))
            if interest['GPA']['Math'] == 'AP':
                self.twelfth.append(self.storage.get_by_name('Calculus BC', 'AP'))
            else:
                self.twelfth.append(self.storage.get_by_name('Calculus AB', 'AP'))

        elif taken['Math'] == 'Geometry':
            self.ninth.append(self.storage.get_by_name('Algebra 2', interest['GPA']['Math']))
            self.tenth.append(self.storage.get_by_name('Precalculus', interest['GPA']['Math']))
            if interest['GPA']['Math'] == 'AP':
                self.eleventh.append(self.storage.get_by_name('Calculus BC', 'AP'))
                self.twelfth.append(self.storage.get_by_name('Multi', 'KAP'))
            else:
                self.eleventh.append(self.storage.get_by_name('Calculus AB', 'AP'))
                self.eleventh.append(self.storage.get_by_name('Calculus BC', 'AP'))
                self.eleventh.append(self.storage.get_by_name('Study Hall'))

        else:
            self.ninth.append(self.storage.get_by_name('Algebra 1', interest['GPA']['Math']))
            self.tenth.append(self.storage.get_by_name('Geometry', interest['GPA']['Math']))
            self.eleventh.append(self.storage.get_by_name('Algebra 2', interest['GPA']['Math']))
            if interest['Math'] > 5:
                self.twelfth.append(self.storage.get_by_name('Precalculus', interest['GPA']['Math']))
            else:
                self.twelfth.append(self.storage.get_by_name('Statistics', 'AP'))

        # ENGLISH
        self.ninth.append(self.storage.get_by_name('English', interest['GPA']['English'], '9th'))
        self.tenth.append(self.storage.get_by_name('English', interest['GPA']['English'], '10th'))
        self.eleventh.append(self.storage.get_by_name('English', interest['GPA']['English'], '11th'))
        self.twelfth.append(self.storage.get_by_name('English', interest['GPA']['English'], '12th'))

        # HISTORY
        if interest['History'] > 5:
            self.ninth.append(self.storage.get_by_name('Human Geography', 'AP'))
        else:
            self.ninth.append(self.storage.get_by_name('World Geography', interest['GPA']['History']))
        self.tenth.append(self.storage.get_by_name('World History', interest['GPA']['History']))
        self.eleventh.append(self.storage.get_by_name('US History', interest['GPA']['History']))
        if interest['History'] > 5:
            self.twelfth.append(self.storage.get_by_name('Macro', 'AP'))
            self.twelfth.append(self.storage.get_by_name('US Government', 'AP'))
        else:
            self.twelfth.append(self.storage.get_by_name('Econ', 'Dual'))
            self.twelfth.append(self.storage.get_by_name('Gov', 'Dual'))

        # SCIENCE
        self.ninth.append(self.storage.get_by_name('Biology', interest['GPA']['Science'], '9th'))
        self.tenth.append(self.storage.get_by_name('Chemistry', interest['GPA']['Science'], '10th'))

        if interest['Medical'] > interest['Engineering']:
            self.eleventh.append(self.storage.get_by_name('Biology', 'AP', '11th'))
            if interest['Engineering'] > 5:
                self.twelfth.append(self.storage.get_by_name('Physics 1', interest['GPA']['Science'], '11th'))
            elif interest['GPA']['Science'] == 'AP':
                self.twelfth.append(self.storage.get_by_name('Chemistry', 'AP', '11th'))
            else:
                self.twelfth.append(self.storage.get_by_name('Environmental', 'AP', '11th'))

        elif interest['Medical'] == interest['Engineering']:
            self.eleventh.append(self.storage.get_by_name('Biology', 'AP'))
            if interest['Engineering'] > 7:
                self.twelfth.append(self.storage.get_by_name('Physics 1', interest['GPA']['Science'], '12th'))
            elif interest['GPA']['Science'] == 'AP':
                self.twelfth.append(self.storage.get_by_name('Chemistry', 'AP', '11th'))
            else:
                self.twelfth.append(self.storage.get_by_name('Environmental', 'AP', '11th'))
        else:
            self.eleventh.append(self.storage.get_by_name('Physics 1', interest['GPA']['Science']))
            self.twelfth.append(self.storage.get_by_name('Physics 2', 'AP'))

        # ELECTIVES

        # FINE ARTS
        if interest['Fine Arts'] > 6:
            self.ninth.append(self.storage.get_by_name(fine_arts, grade='9th'))
            self.tenth.append(self.storage.get_by_name(fine_arts, grade='10th'))
            self.eleventh.append(self.storage.get_by_name(fine_arts, grade='11th'))
            self.twelfth.append(self.storage.get_by_name(fine_arts, grade='12th'))
        elif interest['Fine Arts'] > 2:
            self.ninth.append(self.storage.get_by_name(fine_arts, grade='9th'))
        else:
            self.twelfth.append(self.storage.get_by_name('Art History', 'AP'))

        # PUBLIC SPEAKING

        if interest['Public Speaking'] > 5:
            self.tenth.append(self.storage.get_by_name('Seminar', 'AP'))
            if interest['Public Speaking'] > 7:
                self.eleventh.append(self.storage.get_by_name('Research', 'AP'))
        else:
            self.twelfth.append(self.storage.get_by_name('Professional Communications', ''))

        # OTHER
        #if interest['CS'] > 7:
        #    self.ninth.append(self.storage.get_by_name())

    def print_schedule(self):
        print('Ninth:')
        for i in range(len(self.ninth)):
            print(self.ninth[i])
        print()
        print('Tenth:')
        for i in range(len(self.tenth)):
            print(self.tenth[i])
        print()
        print('Eleventh:')
        for i in range(len(self.eleventh)):
            print(self.eleventh[i])
        print()
        print('Twelfth:')
        for i in range(len(self.twelfth)):
            print(self.twelfth[i])
