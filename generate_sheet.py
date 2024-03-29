from pylatex import Document, Package, Center, NoEscape
import os

# Import class files for different question types
from basic_operations import Multiply, Divide, FractionAdd, FractionSubtract, FractionMultiply
from derivatives import FirstPrinciples, SimpleDerivatives, ChainRule


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
    doc.append(NoEscape(r'\opset{voperation=top}'))

    # Define the document's title
    doc_title = "Grade %s Worksheet" % str(info["grade"])
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

    print(info["topics"])

    # Save files to the student's folder
    path = './' + info["name"]
    if not os.path.isdir(path):
        os.makedirs(path)

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

    if len(topic_list) == 1:
        topic_str = str(topic_list[0])

    else:
        for topic in topic_list:
            if str(topic) != str(topic_list[-1]):
                if str(topic) != str(topic_list[0]):
                    topic_str = topic_str + str(topic).lower() + ", "
                else:
                    topic_str = topic_str + str(topic) + ", "
            else:
                topic_str = topic_str[:-2] + " and " + str(topic).lower()

    # Insert it, centred an in italics
    questions.append(NoEscape(r"\begin{center} \textit{%s} \end{center}" % topic_str))

    # Insert question LaTeX code
    for topic in topic_list:
        topic.insert_question(questions)

    # Generate pdf of question sheet
    questions.generate_pdf(filepath=path+"/"+questions_filename, clean_tex=False)

    # Answers sheet
    # Prepare document name and insert templating
    answers_filename = info["name"] + "-answers"
    answers = basic_formatting(info=info, answers=True)

    # Insert answer LaTeX code
    for topic in topic_list:
        topic.insert_answer(answers)

    # Generate pdf
    answers.generate_pdf(filepath=path+"/"+answers_filename, clean_tex=False)

    return path + "/" + questions_filename + ".pdf", path + "/" + answers_filename + ".pdf"


""" Sample class
class <Topic>:

    @staticmethod
    def leading_text():
        # Text to attach to the front of the question. "Solve this"
        return "Solve me"

    @staticmethod
    def default_num:
        # Default number of this question to include in a worksheet.
        return 8

    def __str__(self):
        # Name of the topic, suitable to print to topic blurb
        return "Topic"

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
            return doc

    def insert_answer(self, doc):
        with doc.create(Section(str(self))):
            # Generate the LaTeX code to insert each worked answer of this topic into the
            # document. 
            return doc
"""


