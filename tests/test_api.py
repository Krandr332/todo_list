import unittest
from app import create_app, db
from app.models import Task
from flask import current_app

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/test_db'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()



    def test_create_task(self):
        with self.app.app_context():
            response = self.client.post('/tasks', json={
                'title': 'Test Task',
                'description': 'This is a test task'
            })
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertIn('id', data)
            self.assertEqual(data['title'], 'Test Task')
            self.assertEqual(data['description'], 'This is a test task')

    def test_get_tasks(self):
        with self.app.app_context():
            response = self.client.get('/tasks')
            self.assertEqual(response.status_code, 200)

    def test_get_task(self):
        with self.app.app_context():
            task = Task(title='Test Task')
            db.session.add(task)
            db.session.commit()
            response = self.client.get(f'/tasks/{task.id}')
            self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        with self.app.app_context():
            task = Task(title='Test Task')
            db.session.add(task)
            db.session.commit()
            response = self.client.put(f'/tasks/{task.id}', json={
                'title': 'Updated Task'
            })
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['title'], 'Updated Task')



if __name__ == '__main__':
    unittest.main()
