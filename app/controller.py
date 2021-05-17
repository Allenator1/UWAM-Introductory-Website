from app.models import User, Quiz
from app import db

FINANCE_ANSWERS = {'Q1':'c', 'Q2':'b', 'Q3':'a'}
MARKETING_ANSWERS = {'Q1':'a', 'Q2':'d', 'Q3':'d'}
VD_ANSWERS = {'Q1':'d', 'Q2':['a', 'b', 'c'], 'Q3':['c', 'd']}
CHASSIS_ANSWERS = {'Q1':'b', 'Q2':'b', 'Q3':'a'}
POWERTRAIN_ANSWERS = {'Q1':['a', 'c'], 'Q2':'d', 'Q3':'c'}

#--------------FUNCTIONS FOR ACCESSING QUIZ DATA------------------

def get_section_totals(quiz):
    section_totals = {} 
    section_totals['Finance'] = get_total(quiz.finance, FINANCE_ANSWERS)
    section_totals['Marketing'] = get_total(quiz.marketing, MARKETING_ANSWERS)
    section_totals['Chassis'] = get_total(quiz.chassis, CHASSIS_ANSWERS)
    section_totals['Vehicle Dynamics'] = get_total(quiz.vehicle_dynamics, VD_ANSWERS)
    section_totals['Powertrain'] = get_total(quiz.powertrain, POWERTRAIN_ANSWERS)
    return section_totals


def get_proportions(totals):
    num_marks = sum(totals.values())
    percents = {}
    for k in totals.keys():
        percents[k] = totals[k] / num_marks * 100
    return percents


def get_total(section, answers):
    total = 0
    for key, val in section.items():
        if type(val) == list and set(val) == set(answers[key]):
            total += 1
        elif type(val) == str and val == answers[key]:
            total += 1
    return total


def is_completed(quiz):
    finance = check_completion(quiz.finance)
    marketing = check_completion(quiz.marketing)
    chassis = check_completion(quiz.chassis)
    vehicle_dynamics = check_completion(quiz.vehicle_dynamics)
    powertrain = check_completion(quiz.powertrain)
    return finance and marketing and chassis and vehicle_dynamics and powertrain


def check_completion(section):
    for k, v in section.items():
        if v == '':
            return False
    return True




