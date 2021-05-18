import unittest
import os
from datetime import datetime
from app import app, db
from app.models import User, Quiz
from app.controller import *


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        user = User(id=1, username="john_1", email="john@example.com", preferred_name="john")
        db.session.add(user)
        db.session.commit()
        quiz = Quiz(id=1, user_id=1)
        db.session.add(quiz)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_user_password_hashing(self):
        user = User.query.get(1)
        user.set_password('test')
        self.assertTrue(user.check_password('test'))
        self.assertFalse(user.check_password('anything else'))


    def test_user_columns(self):
        user = User.query.get(1)
        quiz = Quiz.query.get(1)
        current_quiz = user.current_quiz
        self.assertEqual(current_quiz, None)
        submissions = user.submissions
        self.assertEqual(submissions, [quiz])
        current_tut = user.current_module
        self.assertEqual(current_tut, 'tutorial1')


    def test_quiz_columns(self):
        quiz = Quiz.query.get(1)
        self.assertEqual(quiz.finance, {'Q1': '', 'Q2': '', 'Q3': ''})
        self.assertEqual(quiz.marketing, {'Q1': '', 'Q2': '', 'Q3': ''})
        self.assertEqual(quiz.chassis, {'Q1': '', 'Q2': '', 'Q3': ''})
        self.assertEqual(quiz.vehicle_dynamics, {'Q1': '', 'Q2': '', 'Q3': ''})
        self.assertEqual(quiz.powertrain, {'Q1': '', 'Q2': '', 'Q3': ''})
        self.assertNotEqual(quiz.start_date, None)
        self.assertEqual(quiz.finish_date, None)



class ControllerTestCase(unittest.TestCase):
    
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        user = User(id=1, username="john_1", email="john@example.com", preferred_name="john")
        db.session.add(user)
        db.session.commit()
        quiz = Quiz(id=1, user_id=1)
        db.session.add(quiz)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_get_total(self):
        section = VD_ANSWERS
        total = get_total(section, VD_ANSWERS)
        self.assertEqual(total, 3)

        section = {'Q1': '', 'Q2': '', 'Q3': ''}
        total = get_total(section, VD_ANSWERS)
        self.assertEqual(total, 0)

        section = {'Q1': 'd', 'Q2': ['b', 'a', 'c'], 'Q3': ['c']}
        total = get_total(section, VD_ANSWERS)
        self.assertEqual(total, 1)


    def test_get_completion(self):
        section = {'Q1': '', 'Q2': '', 'Q3': ''}
        self.assertFalse(check_completion(section))
        section = {'Q1': 'a', 'Q2': 'b', 'Q3': ''}
        self.assertFalse(check_completion(section))
        section = {'Q1': 'a', 'Q2': 'b', 'Q3': 'c'}
        self.assertTrue(check_completion(section))
    

    def test_is_completed(self):
        quiz = Quiz.query.get(1)
        self.assertFalse(is_completed(quiz))

        quiz = Quiz.query.get(1)
        quiz.finance = FINANCE_ANSWERS
        quiz.marketing = MARKETING_ANSWERS
        quiz.chassis = CHASSIS_ANSWERS
        quiz.vehicle_dynamics = VD_ANSWERS
        quiz.powertrain = POWERTRAIN_ANSWERS

        self.assertTrue(is_completed(quiz))


    def test_get_totals(self):
        quiz = Quiz.query.get(1)
        totals = get_section_totals(quiz)
        self.assertEqual(totals, {'Finance': 0, 'Marketing': 0, 'Chassis': 0, 
            'Vehicle Dynamics': 0, 'Powertrain': 0})

        quiz.finance = FINANCE_ANSWERS
        quiz.marketing = MARKETING_ANSWERS
        quiz.chassis = CHASSIS_ANSWERS
        quiz.vehicle_dynamics = VD_ANSWERS
        quiz.powertrain = POWERTRAIN_ANSWERS

        totals = get_section_totals(quiz)
        self.assertEqual(totals, {'Finance': 3, 'Marketing': 3, 'Chassis': 3, 
            'Vehicle Dynamics': 3, 'Powertrain': 3})

    
    def test_get_proportions(self):
        quiz = Quiz.query.get(1)
        totals = get_section_totals(quiz)
        props = get_proportions(totals)
        self.assertEqual(props, {'Finance': 0, 'Marketing': 0, 'Chassis': 0, 
            'Vehicle Dynamics': 0, 'Powertrain': 0})

        quiz.finance = FINANCE_ANSWERS
        quiz.marketing = MARKETING_ANSWERS
        quiz.chassis = CHASSIS_ANSWERS
        quiz.vehicle_dynamics = VD_ANSWERS
        quiz.powertrain = POWERTRAIN_ANSWERS

        totals = get_section_totals(quiz)
        props = get_proportions(totals)
        self.assertEqual(props, {'Finance': 20, 'Marketing': 20, 'Chassis': 20, 
            'Vehicle Dynamics': 20, 'Powertrain': 20})



class RouteHandlerTestCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        user = User(id=1, username="john_1", email="john@example.com", preferred_name="john")
        db.session.add(user)
        db.session.commit()
        quiz = Quiz(id=1, user_id=1)
        db.session.add(quiz)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_login_route(self):
        user = User.query.get(1)
        user.set_password('password')
        db.session.commit()
        form = {'username': 'john_1', 'password': 'password'}
        user = User.query.filter_by(username=form['username']).first()
        is_form_invalid = not user or not user.check_password(form['password'])
        self.assertFalse(is_form_invalid)


    def test_register_route(self):
        form = {'username': 'katie-1', 'email':'kate@example.com', 
            'preferred_name':'katie', 'password': 'password'}
        user = User(username=form['username'], email=form['email'])
        if not form['preferred_name']:
            user.preferred_name = user.username
        else:
            user.preferred_name = form['preferred_name']
        user.set_password(form['password'])
        self.assertTrue(user.check_password('password'))
        self.assertEqual(user.username, form['username'])
        self.assertEqual(user.email, form['email'])
        self.assertEqual(user.preferred_name, form['preferred_name'])

        form = {'username': 'katie-1', 'email':'kate@example.com', 
            'preferred_name':'', 'password': 'password'}
        user = User(username=form['username'], email=form['email'])
        if not form['preferred_name']:
            user.preferred_name = user.username
        else:
            user.preferred_name = form['preferred_name']
        user.set_password(form['password'])
        self.assertEqual(user.preferred_name, user.username)


    def test_validate_registration_route(self):
        json = {'username': 'john_1'}
        if json and 'username' in json.keys():
            username = json['username']
            username_available = User.query.filter_by(username=username).first() == None
            self.assertFalse(username_available)

        json = {'username': 'john_2'}
        if json and 'username' in json.keys():
            username = json['username']
            username_available = User.query.filter_by(username=username).first() == None
            self.assertTrue(username_available)

        json = {'username': ''}
        if json and 'username' in json.keys():
            username = json['username']
            username_available = User.query.filter_by(username=username).first() == None
            self.assertTrue(username_available)

        json = {'email': 'john@example.com'}
        if json and 'email' in json.keys():
            email = json['email']
            email_available = User.query.filter_by(email=email).first() == None
            self.assertFalse(email_available)
        
    
    def test_feedback_route(self):
        user = User.query.get(1)
        quiz = Quiz.query.get(1)
        quiz.finish_date = datetime.utcnow()
        quiz.finance = FINANCE_ANSWERS
        db.session.commit()
        quiz = db.session.query(Quiz).join(User).\
            filter(Quiz.user_id == user.id, Quiz.finish_date != None).\
            order_by(Quiz.finish_date.desc()).first()
        self.assertEqual(quiz, Quiz.query.get(1))

        section_totals = get_section_totals(quiz)
        section_proportions = get_proportions(section_totals)
        section = max(section_totals, key=section_totals.get)
        self.assertEqual(section, 'Finance')


    def test_submissions_route(self):
        user = User.query.get(1)
        quiz = Quiz.query.get(1)
        quiz.finish_date = datetime.utcnow()
        quiz.finance = FINANCE_ANSWERS
        db.session.commit()

        submissions = db.session.query(Quiz).join(User).\
        filter(Quiz.user_id == user.id, Quiz.finish_date != None).\
        order_by(Quiz.finish_date.desc()).limit(12).all()
        self.assertEqual(len(submissions), 1)

        submission_stats = []
        aggr_section_totals = {'Finance': 0, 'Marketing': 0, 'Chassis': 0, 'Vehicle Dynamics': 0, 'Powertrain': 0}

        for quiz in submissions:
            stats = {}
            stats['date'] = quiz.finish_date
            stats['quiz_id'] = quiz.id
            section_totals = get_section_totals(quiz)
            aggr_section_totals = {k:(aggr_section_totals[k] + section_totals[k]) for k in section_totals.keys()}
            stats['section'] = max(section_totals, key=section_totals.get)
            stats['time_taken'] = round((quiz.finish_date - quiz.start_date).total_seconds() / 60, 2)
            stats['score'] = sum(section_totals.values())
            submission_stats.append(stats)
        section = max(section_totals, key=aggr_section_totals.get)
        
        self.assertEqual(submission_stats[0]['section'], 'Finance')
        self.assertEqual(section, 'Finance')
        self.assertEqual(submission_stats[0]['score'], 3)

    
    def test_quiz_route(self):
        user = User.query.get(1)
        user.current_quiz = 1
        db.session.commit()

        quiz = self.quiz_test_func(0)
        self.assertEqual(quiz, Quiz.query.get(1))

        user.current_quiz = None
        db.session.commit()

        quiz = self.quiz_test_func(0)
        self.assertEqual(quiz, Quiz.query.get(2))

        user.current_quiz = 1
        quiz = Quiz(id=3, user_id=user.id)
        db.session.commit()

        quiz = self.quiz_test_func(3)
        self.assertEqual(quiz, Quiz.query.get(3))


    def quiz_test_func(self, quiz_id):
        user = User.query.get(1)
        is_new_quiz = int(quiz_id) == 0
        quiz = None
        if not is_new_quiz:
            quiz = Quiz.query.get(quiz_id)
        elif is_new_quiz and not user.current_quiz:
            quiz = Quiz(user_id=user.id)
            db.session.add(quiz)
            db.session.commit()
            user.current_quiz = quiz.id
        elif is_new_quiz and user.current_quiz:    
            quiz = Quiz.query.get(user.current_quiz)
        return quiz
    

    def test_new_quiz_route(self):
        user = User.query.get(1)
        user.current_quiz = 1
        old_quiz = Quiz.query.get(user.current_quiz)
        db.session.delete(old_quiz)
        user.current_quiz = None
        db.session.commit()
        self.assertEqual(user.current_quiz, None)
        self.assertEqual(Quiz.query.get(1), None)


    def test_save_answer_route(self):
        quiz = Quiz.query.get(1)
        quiz.vehicle_dynamics = {'Q1': 'a', 'Q2': '', 'Q3': ['c']}
        db.session.commit()
        self.save_answer_test_func({'vehicle_dynamics-Q2-b': ['on', 'b']})
        self.assertEqual(quiz.vehicle_dynamics, {'Q1': 'a', 'Q2': ['b'], 'Q3': ['c']})

        quiz.vehicle_dynamics = {'Q1': 'a', 'Q2': '', 'Q3': ['c']}
        db.session.commit()
        self.save_answer_test_func({'vehicle_dynamics-Q3-b': ['on', 'a']})
        self.assertEqual(quiz.vehicle_dynamics, {'Q1': 'a', 'Q2': '', 'Q3': ['c', 'a']})

        quiz.vehicle_dynamics = {'Q1': 'a', 'Q2': '', 'Q3': ['c']}
        db.session.commit()
        self.save_answer_test_func({'vehicle_dynamics-Q3-b': ['off', 'c']})
        self.assertEqual(quiz.vehicle_dynamics, {'Q1': 'a', 'Q2': '', 'Q3': []})

        quiz.vehicle_dynamics = {'Q1': 'a', 'Q2': '', 'Q3': []}
        db.session.commit()
        self.save_answer_test_func({'vehicle_dynamics-Q3-b': ['off', 'c']})
        self.assertEqual(quiz.vehicle_dynamics, {'Q1': 'a', 'Q2': '', 'Q3': []})

        quiz.vehicle_dynamics = {'Q1': 'a', 'Q2': '', 'Q3': ['c']}
        db.session.commit()
        self.save_answer_test_func({'vehicle_dynamics-Q1': 'b'})
        self.assertEqual(quiz.vehicle_dynamics, {'Q1': 'b', 'Q2': '', 'Q3': ['c']})

    
    def save_answer_test_func(self, response_dict):
        quiz = Quiz.query.get(1)
        key = list(response_dict.keys())[0]
        department = key.split('-')[0]
        question = key.split('-')[1]

        if len(key.split('-')) > 2:
            response = response_dict[key]
            answer = response[1]
            is_toggled = response[0] == "on"
            current_ans_list = getattr(quiz, department)[question]
            answer_exists = answer in current_ans_list

            if current_ans_list == "" and is_toggled:
                current_ans_list = [answer]
            elif not answer_exists and is_toggled:
                current_ans_list.append(answer)
            elif answer_exists and not is_toggled:
                current_ans_list.remove(answer)

            getattr(quiz, department)[question] = current_ans_list
        else:
            getattr(quiz, department)[question] = response_dict[key]
        db.session.commit()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ModelTestCase('test_user_password_hashing'))
    return suite


if __name__ == '__main__':
    unittest.main()