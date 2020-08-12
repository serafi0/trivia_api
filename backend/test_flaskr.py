import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# two test for retriving questions
    
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    def test_404_request_beyond_valid_page(self):

        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

##two test for question creation

    def test_create_new_question(self):
        new_question =   {
            'question': "will this test pass ?",
            'answer': "I hope it does.",
            'category': "pop",
            'difficulty': 44
        }

        res = self.client().post('/questions',json=new_question)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)


    
    def test_422_if_question_creation_fails(self):
        wrong_question =   {
            'question': "will this test pass ?",
            'answer': "I hope it does not.",
            'category': 44,
            'difficulty': "wrong"
        }


        res = self.client().post('/questions',json=wrong_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)




## two tests for deletion
    def test_404_if_question_does_not_exist(self):

        
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_book(self):

        question = Question(question="will this test pass ?",
                            answer= "I hope it does.",
                            category= "pop",
                            difficulty= 44,

                            )
        question.insert()
                    
        id=question.id

        res = self.client().delete('/questions/{}'.format(id))
        data = json.loads(res.data)
        
        #check if it's deleted
        question = Question.query.filter(Question.id == id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()