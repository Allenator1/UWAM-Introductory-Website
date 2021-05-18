import unittest, os
from app import app, db
from app.models import User, Quiz
from app.controller import *


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
        db.create_all()
        user = User(id=1, username="john_1", email="john@example.com", preferred_name="john")
        db.session.add(user)
        db.session.commit()
        quiz = User(id=1, user_id=1)
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
        self.assertEqual(total, 2)


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

        db.session.commit()
        self.assertTrue(is_completed(quiz))


    def test_get_totals(self):
        quiz = Quiz.query.get(1)
        totals = get_section_totals(quiz)
        self.assertEqual(totals, {'Finance': 0, 'Marketing': 0, 'Chassis': 0, 
            'Vehicle Dynamics': 0, 'Powertrain': 0})

        quiz = Quiz.query.get(1)
        quiz.finance = FINANCE_ANSWERS
        quiz.marketing = MARKETING_ANSWERS
        quiz.chassis = CHASSIS_ANSWERS
        quiz.vehicle_dynamics = VD_ANSWERS
        quiz.powertrain = POWERTRAIN_ANSWERS
        db.session.commit()

        totals = get_section_totals(quiz)
        self.assertEqual(totals, {'Finance': 3, 'Marketing': 3, 'Chassis': 3, 
            'Vehicle Dynamics': 3, 'Powertrain': 3})

    
    def test_get_proportions(self):
        quiz = Quiz.query.get(1)
        totals = get_section_totals(quiz)
        props = get_proportions(totals)
        self.assertEqual(props, {'Finance': 0, 'Marketing': 0, 'Chassis': 0, 
            'Vehicle Dynamics': 0, 'Powertrain': 0})

        quiz = Quiz.query.get(1)
        quiz.finance = FINANCE_ANSWERS
        quiz.marketing = MARKETING_ANSWERS
        quiz.chassis = CHASSIS_ANSWERS
        quiz.vehicle_dynamics = VD_ANSWERS
        quiz.powertrain = POWERTRAIN_ANSWERS
        db.session.commit()

        totals = get_section_totals(quiz)
        props = get_proportions(totals)
        self.assertEqual(props, {'Finance': 100, 'Marketing': 100, 'Chassis': 100, 
            'Vehicle Dynamics': 100, 'Powertrain': 100})


class RouteHandlerTestCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI']=\
            'sqlite:///'+os.path.join(basedir,'test.db')
        self.app = app.test_client()
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




    

