import unittest
from faker import Faker
from app import create_app, blueprint_config, db

class testApi(unittest.TestCase):
    def setUp(self):
        # Set up the app and the app context
        self.app = create_app('DevelopmentConfig')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        
        with self.app.app_context():
            blueprint_config(self.app)  # Register blueprints
            db.create_all()  # Create the database tables

        self.client = self.app.test_client()
        self.fake = Faker()

    # def tearDown(self):
    #     # Tear down the app context and drop the database
    #     with self.app.app_context():
    #         db.drop_all()

    def test_customer(self):
        # Generate fake customer data
        name = self.fake.name()
        email = self.fake.email()
        username = self.fake.user_name()
        password = self.fake.password()
        role_id = self.fake.random_int(min=1, max=2)
        payload = {
            "name": name,
            "email": email,
            "phone": self.fake.phone_number(),
            "username": username,
            "password": password,
            "role_id": role_id
        }

        # Send a POST request to create a new customer
        response = self.client.post('/customers/', json=payload)

        # Print out response content and status for debugging
        print(response)
        print(response.status_code)
        print(response.data)

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Now try to parse the JSON response
        data = response.get_json()

        # Check if the response contains JSON data
        self.assertIsNotNone(data, "Response did not contain JSON data")

        self.assertEqual(data['name'], name)
        self.assertEqual(data['email'], email)
    
    def test_customeraccnt(self):
        # Generate fake customer data
        username = self.fake.user_name()
        password = self.fake.password()
        customer_id = self.fake.random_number(1,10)
        payload = {
            "username": username,
            "password": password,
            "customer_id": customer_id
        }

        # Send a POST request to create a new customer
        response = self.client.post('/customeraccnt/', json=payload)

        # Print out response content and status for debugging
        print(response)
        print(response.status_code)
        print(response.data)

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Now try to parse the JSON response
        data = response.get_json()

        # Check if the response contains JSON data
        self.assertIsNotNone(data, "Response did not contain JSON data")

        self.assertEqual(data['username'], payload["username"])
        self.assertEqual(data['password'], payload["password"])

    def test_order(self):
        # Generate fake customer data

         # Generate fake customer data
        name = self.fake.name()
        email = self.fake.email()
        username = self.fake.user_name()
        password = self.fake.password()
        role_id = self.fake.random_int(min=1, max=2)
        payload = {
            "name": name,
            "email": email,
            "phone": self.fake.phone_number(),
            "username": username,
            "password": password,
            "role_id": role_id
        }

        # Send a POST request to create a new customer
        response = self.client.post('/customers/', json=payload)

        # Print out response content and status for debugging
        print(response)
        print(response.status_code)
        print(response.data)

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Now try to parse the JSON response
        data = response.get_json()
        #customer_id = data["id"]

        # order payload
        payload = {
            "customer_id": self.fake.random_int(min=1, max=20),
            "date": self.fake.date(),
            "products": [
            {"id": self.fake.random_number(1, 5), "name":self.fake.name(),"price":self.fake.random_number(1, 40)},
            {"id": self.fake.random_number(1, 5), "name":self.fake.name(),"price":self.fake.random_number(1, 40)}
        ]
        }

        # Send a POST request to create a new customer
        response = self.client.post('/orders/', json=payload)

        # Print out response content and status for debugging
        print(response)
        print(response.status_code)
        print(response.data)

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Now try to parse the JSON response
        data = response.get_json()

        # Check if the response contains JSON data
        self.assertIsNotNone(data, "Response did not contain JSON data")

        #self.assertEqual(data['date'], payload['date'])

if __name__ == '__main__':
    unittest.main()