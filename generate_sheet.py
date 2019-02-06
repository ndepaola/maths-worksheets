import numpy as np
import matplotlib as mpl
from pylatex import Document, Section, Head, Foot, PageStyle, NoEscape, Command, Package, Subsection
import random
import os

def basic_formatting(doc, info, answers):
    # Basic templating common to both question and answer sheets
    # Import packages
    doc.packages.append(Package("fancyhdr"))
    doc.packages.append(Package("amsmath"))
    doc.packages.append(Package("amssymb"))
    doc.packages.append(Package("microtype"))
    doc.packages.append(Package("multicol"))
    doc.packages.append(Package("xlop"))

    # Define the document's title
    doc_title = "Grade %d Worksheet" % info["grade"]
    if answers:
        doc_title = doc_title + " Answers"

    # Create header
    doc.append(NoEscape(r'\thispagestyle{fancy}'))
    doc.append(NoEscape(r'\lhead{%s}' % info['name']))
    doc.append(NoEscape(r'\chead{%s}' % doc_title))
    doc.append(NoEscape(r'\rhead{\today}'))

    doc.append(NoEscape(r'\newcommand{\gobble}[1]{}'))

    return doc



# Some basic code for making a LaTeX doc with pylatex
def generate_sheet(info):
    geometry_options = {"margin": "1in"}

    # Question sheet
    # Prepare doc variable and insert templating
    questions_filename = info["name"] + "-questions"
    questions = Document(geometry_options=geometry_options)
    questions = basic_formatting(questions, info, False)

    # A sample section and some text
    question_1 = Multiply(6)
    question_2 = Divide(6)

    question_1.insert_question(questions)
    question_2.insert_question(questions)


    # Generate pdf
    questions.generate_pdf(questions_filename, clean_tex=False)

    # Answers sheet
    # Prepare doc variable and insert templating
    answers_filename = info["name"] +  "-answers"
    answers = Document(geometry_options=geometry_options)
    answers = basic_formatting(answers, info, True)

    # Sample tex code
    # with answers.create(Section("The simple stuff")):
    #     answers.append('Some regular text')
    question_1.insert_answer(answers)
    question_2.insert_answer(answers)
    # question_2.insert_answer(answers)

    # Generate pdf
    answers.generate_pdf(answers_filename, clean_tex=False)


def rparam(a, b, p):
    # Return a random number between a and b, with p decimal places of precision
    return round(a + (b-a)*random.random(), p)


class Multiply:
    # Grade 6 long multiplication
    a = []
    b = []

    def leading_text(self):
        return "Calculate the following multiplications:"

    def __str__(self):
        return "Multiplication"

    def __init__(self, n):
        for i in range (0, n):
            # Generate n multiplication problems
            self.a.append(rparam(11, 49, 0))  # first number to multiply between 11 and 49
            self.b.append(rparam(50, 500, 0))  # second number to multiply between 50 and 50000

    def insert_question(self, doc):
        with doc.create(Subsection(str(self), numbering=False)):
            doc.append(self.leading_text())

            doc.append(NoEscape(r'\begin{multicols}{3}'))
            doc.append(NoEscape(r'\begin{enumerate}'))
            for i in range(0, len(self.a)):
                doc.append(NoEscape(r'\item \opmul[displayintermediary=None, resultstyle=\gobble]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Subsection(str(self), numbering=False)):

            doc.append(NoEscape(r'\begin{multicols}{3}'))
            doc.append(NoEscape(r'\begin{enumerate}'))
            for i in range(0, len(self.a)):
                doc.append(NoEscape('\item \opmul[style=display, displayintermediary=all]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc


class Divide:

    # Grade 6 long division
    # Multiply a and b

    def leading_text(self):
        return "Calculate the following divisions:"

    def __str__(self):
        return "Division"

    a = []
    b = []

    # Construct question object
    def __init__(self, n):
        for i in range(0, n):
            answer = rparam(1, 50, 1)
            self.b.append(rparam(1, 20, 0))   # first number to multiply between 11 and 49
            self.a.append(self.b[i] * answer)  # second number to multiply between 50 and 50000

    def insert_question(self, doc):
        with doc.create(Subsection(str(self), numbering=False)):
            doc.append(self.leading_text())

            doc.append(NoEscape(r'\begin{multicols}{3}'))
            doc.append(NoEscape(r'\begin{enumerate}'))
            for i in range(0, len(self.a)):
                doc.append(NoEscape(r'\item \opdiv[remainderstyle=\gobble, resultstyle=\gobble]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

    def insert_answer(self, doc):
        with doc.create(Subsection(str(self), numbering=False)):

            doc.append(NoEscape(r'\begin{multicols}{3}'))
            doc.append(NoEscape(r'\begin{enumerate}'))
            for i in range(0, len(self.a)):
                doc.append(NoEscape('\item \opdiv[style=display, displayintermediary=all]{%f}{%f}\qquad' % (self.a[i], self.b[i])))
            doc.append(NoEscape('\end{enumerate}'))
            doc.append(NoEscape('\end{multicols}'))
            return doc

