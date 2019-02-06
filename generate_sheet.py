from pylatex import Document, Package, Center

# Import class files for different question types
from basic_operations import *


def basic_formatting(info, answers):
    geometry_options = {"margin": "1in"}
    doc = Document(geometry_options=geometry_options)

    # Basic templating common to both question and answer sheets
    # Import packages
    doc.packages.append(Package("fancyhdr"))
    doc.packages.append(Package("amsmath"))
    doc.packages.append(Package("amssymb"))
    doc.packages.append(Package("microtype"))
    doc.packages.append(Package("multicol"))
    doc.packages.append(Package("xlop"))
    doc.packages.append(Package("enumitem"))
    doc.packages.append(Package("sectsty"))
    doc.append(NoEscape('\opset{voperation=top}'))

    # Define the document's title
    doc_title = "Grade %d Worksheet" % info["grade"]
    if answers:
        doc_title = doc_title + " Answers"

    # Create header
    doc.append(NoEscape(r'\thispagestyle{fancy}'))
    doc.append(NoEscape(r'\lhead{%s}' % info['name']))
    doc.append(NoEscape(r'\chead{%s}' % doc_title))
    doc.append(NoEscape(r'\rhead{\today}'))

    # Used for questions using xlop to mask the final answer
    doc.append(NoEscape(r'\newcommand{\gobble}[1]{}'))

    # Reduce section font size to size of subsection font
    doc.append(NoEscape(r"\sectionfont{\fontsize{12}{15}\selectfont}"))

    return doc


# Primary entry point into system
def generate_sheet(info):
    # Question sheet
    # Prepare document name and insert templating
    questions_filename = info["name"] + "-questions"
    questions = basic_formatting(info=info, answers=False)

    # Extract all of the requested topics and construct
    # objects with the specified number of questions
    topic_list = []
    for object_type, param in info["topics"]:
        topic_list.append(object_type(param))

    # Create a title blurb with list of topics on sheet
    topic_str = ''
    for topic in topic_list:
        if str(topic) != str(topic_list[-1]):
            topic_str = topic_str + str(topic) + ", "
        else:
            topic_str = topic_str[:-2] + " and " + str(topic).lower()

    # Insert it, centred an in italics
    questions.append(NoEscape(r"\begin{center} \textit{%s} \end{center}" % topic_str))

    # Insert question LaTeX code
    for topic in topic_list:
        topic.insert_question(questions)

    # Generate pdf of question sheet
    questions.generate_pdf(questions_filename, clean_tex=False)

    # Answers sheet
    # Prepare document name and insert templating
    answers_filename = info["name"] + "-answers"
    answers = basic_formatting(info=info, answers=True)

    # Insert answer LaTeX code
    for topic in topic_list:
        topic.insert_answer(answers)

    # Generate pdf
    answers.generate_pdf(answers_filename, clean_tex=False)



