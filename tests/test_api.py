import unittest
from app import create_app, db
from app.models import Task

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_task(self):
        response = self.client.post('/tasks/', json={
            'title': 'Test Task',
            'description': 'This is a test task'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'This is a test task')

    def test_get_tasks(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_get_task(self):
        task = Task(title='Test Task')
        db.session.add(task)
        db.session.commit()
        response = self.client.get(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        task = Task(title='Test Task')
        db.session.add(task)
        db.session.commit()
        response = self.client.put(f'/tasks/{task.id}', json={
            'title': 'Updated Task'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Task')

    def test_delete_task(self):
        task = Task(title='Test Task')
        db.session.add(task)
        db.session.commit()
        response = self.client.delete(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Task deleted successfully')

if __name__ == '__main__':
    unittest.main()
