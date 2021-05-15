from app.models import User, Quiz
from app import db

SECTION1_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}
SECTION2_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)} 
SECTION3_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}
SECTION4_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}
SECTION5_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}

#--------------FUNCTIONS FOR ACCESSING QUIZ DATA------------------

def get_section_totals(quiz):
    section_totals = []
    section_totals.append(get_total(quiz.section1, SECTION1_ANSWERS))
    section_totals.append(get_total(quiz.section2, SECTION2_ANSWERS))
    section_totals.append(get_total(quiz.section3, SECTION3_ANSWERS))
    section_totals.append(get_total(quiz.section4, SECTION4_ANSWERS))
    section_totals.append(get_total(quiz.section5, SECTION5_ANSWERS))
    return section_totals


def get_section_proportions(section_totals):
    percents = []
    num_marks = sum(section_totals)
    for t in section_totals:
        percents.append(t / num_marks * 100)
    return percents


def get_total(questions, answers):
    total = 0
    for key in questions.keys():
        if answers[key].lower() == questions[key].lower():
            total += 1
    return total


