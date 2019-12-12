from unittest import TestCase, main as unittest_main, mock
from app import app
from nose.tools import assert_true
import requests
from bson.objectid import ObjectId
from pymongo import response

sample_id_list = ['k98wesWKOjB','C67iPKLQrEW']
sample_koala_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_koala = {
    'name': 'Tony',
    'description': 'Fluffy.',
    'url': 'https://peopledotcom.files.wordpress.com/2019/05/koalas-2.jpg'
}
sample_form_data = {
    'name': sample_koala['name'],
    'description': sample_koala['description'],
    'url': sample_koala['url']
}

class KoalasTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_index(self):
        """Test the index homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
    
    def test_new(self):
        result = self.client.get('/koalas/new')
        self.assertEqual(result.status, '200 OK')

    def test_request_response(self):
        response = requests.get('https://some-random-api.ml/facts/koala')
        assert_true(response.ok)

    def test_request_response1(self):
        response = requests.get('https://some-random-api.ml/img/koala')
        assert_true(response.ok)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_koala(self, mock_insert):
         """Test submitting a new koala."""
         result = self.client.post('/koalas', data=sample_form_data)
         self.assertEqual(result.status, '302 FOUND')
         mock_insert.assert_called_with(sample_koala)




if __name__ == '__main__':
    unittest_main()