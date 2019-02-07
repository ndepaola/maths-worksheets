from pylatex import Section, NoEscape
import random


def rparam(a, b, p):
    # Parameter generation helper function
    # Return a random number between a and b, with p decimal places of precision
    return round(a + (b-a)*random.random(), p)


""" Sample class
class <Topic>:

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        # return "Solve me"

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb

    def __init__(self, n):
        # Create randomly generated parameters and store them as class variables
        # Parameters should be n-element lists, where n is the number of questions
        # you want to generate of this type.
        # We can also expand the inputs here to include a difficulty setting, and that
        # could affect how parameters are generated.
        # I've included a helper function <rparam> here to make it simpler to generate
        # parameters between a certain range and with a specified decimal precision.
        
    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each question of this topic into the document.
            # Returns doc.
        
    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document. Returns doc.
"""


class Multiply:
    # Long multiplication
    a = []
    b = []

    @staticmethod
    def leading_text():
        return "Calculate the following multiplications:"

    def __str__(self):
        return "Multiplication"

    def __init__(self, n):
        for i in range (0, n):
            # Generate n multiplication problems
            self.a.append(rparam(11, 49, 0))  # first number to multiply between 11 and 49
            self.b.append(rparam(50, 500, 0))  # second number to multiply between 50 and 50000

    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            doc.append(self.leading_text())

            doc.append(NoEscape(r'\begin{multicols}{4}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.a)):
                doc.append(NoEscape(r'\item \opmul[intermediarystyle=\gobble, '
                                    r'resultstyle=\gobble]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            # Insert multiplication answers in 3 columns and itemize
            doc.append(NoEscape(r'\begin{multicols}{4}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))

            # Loop over each stored problem and insert the LaTeX code for the solution
            for i in range(0, len(self.a)):
                doc.append(NoEscape('\item \opmul[style=display, '
                                    'displayintermediary=all]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc


class Divide:
    # Grade 6 long division
    # Divide b by a

    # Leading text to insert into worksheet: "solve this thing"
    @staticmethod
    def leading_text():
        return "Calculate the following divisions:"

    # Return the type of problem as a string
    def __str__(self):
        return "Division"

    # Class variables - list of numbers to divide
    a = []
    b = []

    # Construct question object
    def __init__(self, n):
        for i in range(0, n):
            answer = rparam(1, 50, 1)
            self.b.append(rparam(1, 20, 0))   # first number to multiply between 11 and 49
            self.a.append(self.b[i] * answer)  # second number to multiply between 50 and 50000

    # Attach the LaTeX code for this question to the supplied doc
    def insert_question(self, doc):
        with doc.create(Section(str(self))):
            # Insert leading text
            doc.append(self.leading_text())

            # Wrap in multicols and enumerate
            doc.append(NoEscape(r'\begin{multicols}{4}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.a)):
                doc.append(NoEscape(r'\item \opdiv[remainderstyle=\gobble, '
                                    r'resultstyle=\gobble]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):

            doc.append(NoEscape(r'\begin{multicols}{4}'))
            doc.append(NoEscape(r'\begin{enumerate}[label=(\alph*)]'))
            for i in range(0, len(self.a)):
                doc.append(NoEscape('\item \opdiv[style=display, '
                                    'displayintermediary=all]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc
