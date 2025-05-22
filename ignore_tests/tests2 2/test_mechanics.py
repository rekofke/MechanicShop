from app import create_app
from app.models import db, Mechanic
from app.utils.utils import encode_token
from marshmallow.exceptions import ValidationError
import unittest


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name='John Doe', address='123 test Ave.', email='test@test.com', password='test123' )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token({"user_id": 1})
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_mechanic(self):
        payload = {
            'name': 'test_mechanic',
            'address': '123 test Ave.',
            'email': 'test@test.com',
            'password': 'test123'
        }

        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part_name'], 'test_part')

    def test_create_mechanic_invalid(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.json['message'], 'No mechanics found')
        
    def test_get_mechanics(self):
        response = self.client.get('/mechanics/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_get_mechanic(self):
        response = self.client.get(f'/mechanics/{self.mechanic.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_update_mechanic(self):
        update_payload = {
            'name': 'test_mechanic',
            'address': '123 test Ave.',
            'email': 'test@test.com',
            'password': 'test123'
        }

        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.put(f'/mechanics/{self.mechanic.id}', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Dohn Joe')

    def test_delete_mechanic(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.delete(f'/mechanics/{self.mechanic.id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)