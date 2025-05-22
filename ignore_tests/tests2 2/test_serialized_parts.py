from app import create_app
from app.models import db, SerializedPart, PartDescription
from app.utils.utils import encode_token
from marshmallow.exceptions import ValidationError
import unittest


class TestSerializedParts(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            part_desc = PartDescription(
                id=1, 
                part_name='test_part', 
                brand='test_brand', 
                price=10.99
            )
            db.session.add(part_desc)
            
            self.serialized_part = SerializedPart(desc_id=1, ticket_id=1)
            db.session.add(self.serialized_part)
            db.session.commit()
        
        self.token = encode_token({"user_id": 1})

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_serialized_part(self):
        payload = {
            'desc_id': 1,
            'ticket_id': 1
        }

        response = self.client.post('/serialized_parts/', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], 'test_part')

    def test_get_serialized_parts(self):
        response = self.client.get('/serialized_parts/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['items'][0]['desc_id'], 1)  

    # def test_no_serialized_parts_found(self):
    #     response = self.client.get('/vehicles/')
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json['message'], 'Invalid serialized part')

    def test_get_serialized_parts(self):
        response = self.client.get('/serialized_parts/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['items'][0]['desc_id'], 1)

    def test_update_serialized_part(self):
        update_payload = {
            "id": self.serialized_part.id,
            'desc_id': 1,
            'ticket_id': 1
        }

        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.put(f'/serialized_parts/{self.serialized_part.id}', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['desc_id'], 1)

    def test_delete_serialized_part(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.delete(f'/serialized_parts/{self.serialized_part.id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)