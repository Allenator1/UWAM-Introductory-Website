from app.models import User, Quiz
from app import db

SECTION1_ANSWERS = {'Q' + str(i) : 0 for i in range(1, 6)}
SECTION2_ANSWERS = {'Q' + str(i) : 0 for i in range(1, 6)} 
SECTION3_ANSWERS = {'Q' + str(i) : 0 for i in range(1, 6)}
SECTION4_ANSWERS = {'Q' + str(i) : 0 for i in range(1, 6)}
SECTION5_ANSWERS = {'Q' + str(i) : 0 for i in range(1, 6)}

#--------------FUNCTIONS FOR ACCESSING QUIZ DATA------------------

def get_section_totals(quiz):
    totals = []
    totals.append(get_total(quiz.section1, SECTION1_ANSWERS))
    totals.append(get_total(quiz.section2, SECTION2_ANSWERS))
    totals.append(get_total(quiz.section3, SECTION3_ANSWERS))
    totals.append(get_total(quiz.section4, SECTION4_ANSWERS))
    totals.append(get_total(quiz.section5, SECTION5_ANSWERS))
    return totals

def get_total(questions, answers):
    total = 0
    for key in questions.keys():
        if answers[key].lower() == questions[key].lower():
            total += 1
    return total


