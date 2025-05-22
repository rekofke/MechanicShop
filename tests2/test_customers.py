from app import create_app
from app.utils.utils import encode_token
from marshmallow.exceptions import ValidationError
from app.models import db, Customer
import sqlalchemy
from unittest import TestCase
from app.blueprints.customers.schemas import customer_schema
import unittest



class TestCustomer(unittest.TestCase):

        def setUp(self):
            self.app = create_app()  # Initialize your app
            self.customer = Customer(name='Test', email='test@test.com', phone='1234567890')
            with self.app.app_context():
                db.drop_all()
                db.create_all()
                db.session.add(self.customer)
                db.session.commit()
                self.customer_id = self.customer.id            
                self.client = self.app.test_client()
            self.token = encode_token(1)
            self.client = self.app.test_client()

            # self.valid_token = encode_token({'user_id': 1})
            # self.invalid_token = 'Bearer invalidtoken123' 

        def tearDown(self):
            with self.app.app_context():
                db.session.remove()
                db.drop_all()

        # send test request to endpoint with payload and return response to variable
        def test_add_customer(self):
            payload = {
                'name': 'John Doe',
                'email': 'test@example.com',
                'phone': '503-555-1212'
            }
            response = self.client.post('/customers/', json=payload)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['name'], 'John Doe') # double check the response we get back

        def test_add_invalid_customer(self):
            payload = {
                'name': 'John Doe',
                'phone': '503-555-1212'
            }
            response = self.client.post('/customers/', json=payload)
            self.assertRaises(ValidationError)
            self.assertEqual(response.status_code, 400)
            self.assertIn("email", response.json)

        def test_get_customers(self):
            
            response = self.client.get('/customers/?page=1&per_page=10')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json[0]['name'], 'Test')

        def test_get_customer(self):
             
            response = self.client.get(f'/customers/{self.customer_id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], 'Test')

        
        def test_update_customer(self):
            update_payload = {
                'name': 'new customer',
                'email': 'test@test.com',
                'phone': '1234567890'
            }
            headers = {'Authorization': 'Bearer ' + self.token} 
            response = self.client.put(f'/customers/{self.customer_id}', json=update_payload, headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], 'new customer')  

        def test_delete_customer(self):
            headers = {'Authorization': 'Bearer ' + self.token}
            response = self.client.delete(f'/customers/{self.customer.id}', headers=headers)          
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'message': f'Successfully deleted customer {self.customer_id}'})

            with self.app.app_context():
                deleted_customer = db.session.get(Customer, self.customer_id)
                self.assertIsNone(deleted_customer)