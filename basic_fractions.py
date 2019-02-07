from pylatex import Section, NoEscape
import random
from fractions import Fraction


def rparam(a, b, p):
    # Parameter generation helper function
    # Return a random number between a and b, with p decimal places of precision
    return round(a + (b-a)*random.random(), p)


class FractionAdd:

    a_num = []
    a_den = []
    a = []
    b_num = []
    b_den = []
    b = []

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        # return "Solve me"
        return "Add the following fractions together. Write the answer " \
               "as either an improper fraction or a mixed number."

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb
        return "Adding fractions"

    def __init__(self, n):
        # Create randomly generated parameters and store them as class variables
        # Parameters should be n-element lists, where n is the number of questions
        # you want to generate of this type.
        # We can also expand the inputs here to include a difficulty setting, and that
        # could affect how parameters are generated.
        # I've included a helper function <rparam> here to make it simpler to generate
        # parameters between a certain range and with a specified decimal precision.
        for i in range(0, n):
            if random.random() > 1/3:
                self.a.append(rparam(1, 3, 0))
            else:
                self.a.append(0)
            if random.random() > 1/2:
                self.b.append(rparam(1, 5, 0))
            else:
                self.b.append(0)

            self.a_num.append(rparam(1, 10, 0))
            self.a_den.append(rparam(1, 15, 0))
            self.b_num.append(rparam(1, 10, 0))
            self.b_den.append(rparam(1, 15, 0))

    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            doc.append(self.leading_text())
            # Generate the LaTeX code to insert each question of this topic into the document.
            # Returns doc.
            doc.append(NoEscape(r'\begin{multicols}{4}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.a)):
                frac_string = r'\item $$ '
                if self.a[i] != 0:
                    frac_string += '%i ' % (self.a[i])
                frac_string += r'\frac{%i}{%i} + ' % (self.a_num[i], self.a_den[i])
                if self.b[i] != 0:
                    frac_string += '%i ' % (self.b[i])
                frac_string += r'\frac{%i}{%i} $$' % (self.b_num[i], self.b_den[i])
                doc.append(NoEscape(frac_string))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document. Returns doc.
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.a)):
                # Initial fraction
                frac_string = r'\item $$ '
                if self.a[i] != 0:
                    frac_string += '%i ' % (self.a[i])
                frac_string += r'\frac{%i}{%i} + ' % (self.a_num[i], self.a_den[i])
                if self.b[i] != 0:
                    frac_string += '%i ' % (self.b[i])
                frac_string += r'\frac{%i}{%i} = ' % (self.b_num[i], self.b_den[i])

                # Common denominator
                new_num = 0
                new_den = self.a_den[i] * self.b_den[i]
                if self.a_den[i] == self.b_den[i]:
                    new_den = self.a_den[i]
                    frac_string += r'\frac{%i}{%i} + \frac{%i}{%i} =' % \
                        ((self.a[i] * self.a_den[i]) + self.a_num[i], new_den,
                         (self.b[i] * self.b_den[i]) + self.b_num[i], new_den)

                    # Add numerators
                    new_num = (self.a[i] * self.a_den[i]) + self.a_num[i] + \
                              (self.b[i] * self.b_den[i]) + self.b_num[i]

                else:

                    frac_string += r'\frac{%i}{%i} + \frac{%i}{%i} =' % \
                        (self.b_den[i] * (self.a_num[i] + self.a_den[i] * self.a[i]), new_den,
                         self.a_den[i] * (self.b_num[i] + self.b_den[i] * self.b[i]), new_den)

                    # Add numerators
                    new_num = self.b_den[i] * (self.a_num[i] + self.a_den[i] * self.a[i]) + \
                              self.a_den[i] * (self.b_num[i] + self.b_den[i] * self.b[i])

                frac_string += r'\frac{%i}{%i} = ' % (new_num, new_den)



                final = Fraction(int(new_num), int(new_den))
                if final.denominator > 1:
                    frac_string += r'\frac{%i}{%i} $$' % (final.numerator, final.denominator)
                else:
                    frac_string += r'%i $$' % final.numerator

                doc.append(NoEscape(frac_string))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

class FractionSubtract:

    a_num = []
    a_den = []
    a = []
    b_num = []
    b_den = []
    b = []

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        # return "Solve me"
        return "Subtract the following fractions. Write the answer " \
               "as either an improper fraction or a mixed number."

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb
        return "Subtracting fractions"

    def __init__(self, n):
        # Create randomly generated parameters and store them as class variables
        # Parameters should be n-element lists, where n is the number of questions
        # you want to generate of this type.
        # We can also expand the inputs here to include a difficulty setting, and that
        # could affect how parameters are generated.
        # I've included a helper function <rparam> here to make it simpler to generate
        # parameters between a certain range and with a specified decimal precision.
        for i in range(0, n):
            # 2/3 chance of not having a number out the front of the 1st term
            if random.random() > 1/3:
                self.a.append(rparam(1, 3, 0))
            else:
                self.a.append(0)
            # 1/2 chance of not having a number out the front of the 2nd term
            if random.random() > 1/2:
                self.b.append(rparam(1, 5, 0))
            else:
                self.b.append(0)

            # Generate fraction tops and bottoms
            self.a_num.append(rparam(1, 10, 0))
            self.a_den.append(rparam(1, 15, 0))
            self.b_num.append(rparam(1, 10, 0))
            self.b_den.append(rparam(1, 15, 0))

            # No possibility of negative answers
            while self.b[i] + self.b_num[i]/self.b_den[i] > \
                  self.a[i] + self.a_num[i]/self.a_den[i]:
                if random.random() > 1 / 2:
                    self.b[i] = (rparam(1, 5, 0))
                else:
                    self.b[i] = (0)
                self.b_num[i] = (rparam(1, 10, 0))
                self.b_den[i] = (rparam(1, 15, 0))

    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            doc.append(self.leading_text())
            # Generate the LaTeX code to insert each question of this topic into the document.
            # Returns doc.
            doc.append(NoEscape(r'\begin{multicols}{4}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.a)):
                frac_string = r'\item $$ '
                if self.a[i] != 0:
                    frac_string += '%i ' % (self.a[i])
                frac_string += r'\frac{%i}{%i} - ' % (self.a_num[i], self.a_den[i])
                if self.b[i] != 0:
                    frac_string += '%i ' % (self.b[i])
                frac_string += r'\frac{%i}{%i} $$' % (self.b_num[i], self.b_den[i])
                doc.append(NoEscape(frac_string))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document. Returns doc.
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.a)):
                # Initial fraction
                frac_string = r'\item $$ '
                if self.a[i] != 0:
                    frac_string += '%i ' % (self.a[i])
                frac_string += r'\frac{%i}{%i} - ' % (self.a_num[i], self.a_den[i])
                if self.b[i] != 0:
                    frac_string += '%i ' % (self.b[i])
                frac_string += r'\frac{%i}{%i} = ' % (self.b_num[i], self.b_den[i])

                # Common denominator
                new_den = self.a_den[i] * self.b_den[i]
                if self.a_den[i] == self.b_den[i]:
                    new_den = self.a_den[i]
                    frac_string += r'\frac{%i}{%i} - \frac{%i}{%i} =' % \
                        ((self.a[i] * self.a_den[i]) + self.a_num[i], new_den,
                         (self.b[i] * self.b_den[i]) + self.b_num[i], new_den)

                    # Add numerators
                    new_num = ((self.a[i] * self.a_den[i]) + self.a_num[i]) - \
                              ((self.b[i] * self.b_den[i]) + self.b_num[i])

                else:

                    frac_string += r'\frac{%i}{%i} - \frac{%i}{%i} =' % \
                        (self.b_den[i] * (self.a_num[i] + self.a_den[i] * self.a[i]), new_den,
                         self.a_den[i] * (self.b_num[i] + self.b_den[i] * self.b[i]), new_den)

                    # Add numerators
                    new_num = (self.b_den[i] * (self.a_num[i] + self.a_den[i] * self.a[i])) - \
                              (self.a_den[i] * (self.b_num[i] + self.b_den[i] * self.b[i]))

                frac_string += r'\frac{%i}{%i} = ' % (new_num, new_den)

                final = Fraction(int(new_num), int(new_den))
                if final.denominator > 1:
                    frac_string += r'\frac{%i}{%i} $$' % (final.numerator, final.denominator)
                else:
                    frac_string += r'%i $$' % final.numerator

                doc.append(NoEscape(frac_string))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

