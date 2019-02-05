import numpy as np
import matplotlib as mpl
from pylatex import Document, Section, Head, Foot, PageStyle, NoEscape, Command
import os

# Some basic code for making a LaTeX doc with pylatex
def generate_sheet(info):
    # Basic templating common to both question and answer sheets
    geometry_options = {"margin": "0.8in"}

    # Add document header
    header = PageStyle("header")
    # Create left header
    with header.create(Head("L")):
        header.append(NoEscape(r'\today'))
    # Create right header
    with header.create(Head("R")):
        header.append("Nicholas de Paola Mathematics Tutoring")
    with header.create(Foot("C")):
        header.append(NoEscape(r'\thepage'))

    # Question sheet
    # Prepare doc variable and insert templating
    questions_filename = info["name"] + "-questions"
    questions = Document(geometry_options=geometry_options)
    doc_title = "Grade %d Worksheet" % info["grade"]

    questions.preamble.append(header)
    questions.preamble.append(Command('title', doc_title))
    questions.preamble.append(Command('author', info["name"]))
    questions.preamble.append(Command('date', NoEscape(r'')))
    questions.change_document_style("header")
    questions.append(NoEscape(r'\maketitle'))
    questions.append(NoEscape(r'\thispagestyle{fancy}'))

    # A sample section and some text
    with questions.create(Section("The simple stuff")):
        questions.append('Some regular text')

    # Generate pdf
    questions.generate_pdf(questions_filename, clean_tex=False)

    # Answers sheet
    # Prepare doc variable and insert templating
    answers_filename = info["name"] +  "-answers"
    answers = Document(geometry_options=geometry_options)
    doc_title = "Grade %d Worksheet Answers" % info["grade"]

    answers.preamble.append(header)
    answers.preamble.append(Command('title', doc_title))
    answers.preamble.append(Command('author', info["name"]))
    answers.preamble.append(Command('date', NoEscape(r'')))
    answers.change_document_style("header")
    answers.append(NoEscape(r'\maketitle'))
    answers.append(NoEscape(r'\thispagestyle{fancy}'))

    # Sample tex code
    with answers.create(Section("The simple stuff")):
        answers.append('Some regular text')

    # Generate pdf
    answers.generate_pdf(answers_filename, clean_tex=False)