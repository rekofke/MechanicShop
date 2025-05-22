from app import create_app
from app.models import db, Vehicle, Customer
from app.utils.utils import encode_token
from marshmallow.exceptions import ValidationError
import unittest


class TestVehicles(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.vehicle = Vehicle(make='test_make', model='test_model', customer_id= 1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create a test customer
            customer = Customer(id=1, name="Test Customer", email="test@example.com")
            db.session.add(customer)
            db.session.commit()
            
            # Create a test vehicle
            self.vehicle(make='test_make', model='test_model', customer_id=1)
            db.session.add(self.vehicle)
            db.session.add(self.vehicle)
            db.session.commit()
            
        self.token = encode_token({"user_id": 1})
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_vehicle(self):
        payload = {
            'make': 'test_make',
            'model': 'test_model',
            'customer_id': 1
        }

        response = self.client.post('/vehicles/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['make'], 'test_make')

    def test_get_vehicles(self):
        response = self.client.get('/vehicles/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_vehicle_not_found(self):
        response = self.client.get('/vehicles/999')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid vehicle ID')

    def test_get_vehicle(self):
        response = self.client.get(f'/vehicles/{self.vehicle_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['make'], 'test_make')

    def test_update_vehicle(self):
        update_payload = {
            'make': 'test_make',
            'model': 'test_model',
            'customer_id': 1
        }

        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.put(f'/vehicles/{self.vehicle_id}', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['make'], 'updated_make')

    def test_delete_vehicle(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.delete(f'/vehicles/{self.vehicle_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)