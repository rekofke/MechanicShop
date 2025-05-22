from app import create_app
from app.utils.utils import encode_token
from marshmallow.exceptions import ValidationError
from app.models import db, Mechanic
import unittest
from unittest import TestCase
from werkzeug.security import generate_password_hash



class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.mechanic = Mechanic(name='Test', address='123 Test', email='test@test.com', password=generate_password_hash('123'))
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            self.mechanic_id = self.mechanic.id
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def tearDown(self):
         with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    
    def test_login_mechanic(self):
        payload = {
            'email': 'test@test.com',
            'password': '123'
        }
        response = self.client.post('/mechanics/login', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_mechanic(self):
        payload = {
            'name': 'Test',
            'address': '123 Test',
            'email': 'unique_test@test.com',
            'password': '123'
        }
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Test')

    def test_add_invalid_mechanic(self):
            payload = {
                'name': 'John Doe',
                'address': '123 test Ave.',
                'password': 'test123'
            }
            response = self.client.post('/mechanics/', json=payload)
            self.assertRaises(ValidationError)
            self.assertEqual(response.status_code, 400)
            self.assertIn("email", response.json)

    def test_get_mechanic(self):
            
            response = self.client.get('/mechanics/?page=1&per_page=10')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json[0]['name'], 'Test')

    def test_get_mechanic(self):
                  
            response = self.client.get(f'/mechanics/{self.mechanic_id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], 'Test')

    def test_update_mechanic(self):
        update_payload = {
            'name': 'new mechanic',
            'address': '123 new mechanic',
            'email': 'test@test.com',
            'password': '123'
        }
        headers = {'Authorization': 'Bearer ' + self.token} 
        response = self.client.put('/mechanics/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'new mechanic')

#* NEED TO FIX DELETE TEST CASE
    # def test_delete_mechanic(self):
    #     headers = {'Authorization': 'Bearer ' + self.token}
    #     response = self.client.delete(f'/mechanics/{self.mechanic_id}')
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(response.json['message'], f'successfully deleted mechanic')

        
    # def test_delete_mechanic(self):
    #     headers = {'Authorization': 'Bearer ' + self.token}
    #     response = self.client.delete(f'/mechanics/{self.mechanic.id}', headers=headers)          
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json, {'message': f'Successfully deleted mechanic {self.mechanic_id}'})

    #     with self.app.app_context():
    #         deleted_mechanic = db.session.get(Mechanic, self.mechanic_id)
    #         self.assertIsNone(deleted_mechanic)
