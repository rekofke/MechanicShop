from app import create_app
from app.models import db, Customer
from app.utils.utils import encode_token
from marshmallow.exceptions import ValidationError
import unittest


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(name='John Doe', email='test@test.com', phone='1234567890')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        # self.token = encode_token({"user_id": 1})
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_customer(self):
        payload = {
            'name': 'test_customer',
            'email': 'test@test.com',
            'phone': '1234567890'
        }

        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['part_name'], 'test_part')

    def test_get_customers(self):
        response = self.client.get('/customers/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_get_customer(self):
        response = self.client.get(f'/customers/{self.customer.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_update_customer(self):
        update_payload = {
            'name': 'test_customer',
            'email': 'test@test.com',
            'phone': '1234567890'
        }

        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.put(f'/customers/{self.customer.id}', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Dohn Joe')

    def test_delete_customer(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.delete(f'/customers/{self.customer.id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)