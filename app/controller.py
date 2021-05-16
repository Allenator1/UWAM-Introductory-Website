from app.models import User, Quiz
from app import db

FINANCE_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}
MARKETING_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)} 
VD_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}
CHASSIS_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}
POWERTRAIN_ANSWERS = {'Q' + str(i) : '' for i in range(1, 6)}

#--------------FUNCTIONS FOR ACCESSING QUIZ DATA------------------

def get_section_totals(quiz):
    section_totals = {} 
    section_totals['Finance'] = get_total(quiz.finance, FINANCE_ANSWERS)
    section_totals['Marketing'] = get_total(quiz.marketing, MARKETING_ANSWERS)
    section_totals['Chassis'] = get_total(quiz.chassis, VD_ANSWERS)
    section_totals['Vehicle Dynamics'] = get_total(quiz.vehicle_dynamics, CHASSIS_ANSWERS)
    section_totals['Powertrain'] = get_total(quiz.powertrain, POWERTRAIN_ANSWERS)
    return section_totals


def get_proportions(totals):
    num_marks = sum(totals.values())
    percents = {}
    for k in totals.keys():
        percents[k] = totals[k] / num_marks * 100
    return percents


def get_total(questions, answers):
    total = 0
    for key in questions.keys():
        if answers[key].lower() == questions[key].lower():
            total += 1
    return total


