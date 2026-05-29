"""
Tests para la API de Ticketing
"""
import unittest
import json
from app import create_app
from database import db
from models import User, Ticket
from auth import hash_password


class TicketingAPITestCase(unittest.TestCase):
    
    def setUp(self):
        """Preparar para cada test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Crear usuario de prueba
            user = User(
                username='test_user',
                email='test@example.com',
                password=hash_password('password123')
            )
            db.session.add(user)
            db.session.commit()
            
            self.user_id = user.id
    
    def tearDown(self):
        """Limpiar después de cada test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/v1/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_user_registration(self):
        """Test registro de usuario"""
        response = self.client.post('/api/v1/auth/register',
            data=json.dumps({
                'username': 'new_user',
                'email': 'new@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('access_token', data)
    
    def test_user_login(self):
        """Test login de usuario"""
        response = self.client.post('/api/v1/auth/login',
            data=json.dumps({
                'username': 'test_user',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('access_token', data)
    
    def test_create_ticket(self):
        """Test crear ticket"""
        # Primero hacer login para obtener token
        login_response = self.client.post('/api/v1/auth/login',
            data=json.dumps({
                'username': 'test_user',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['access_token']
        
        # Crear ticket
        response = self.client.post('/api/v1/tickets',
            data=json.dumps({
                'title': 'Test Ticket',
                'description': 'Esta es una descripción de prueba para el ticket'
            }),
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'open')
    
    def test_update_ticket_status(self):
        """Test actualizar estado del ticket"""
        # Login
        login_response = self.client.post('/api/v1/auth/login',
            data=json.dumps({
                'username': 'test_user',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['access_token']
        
        # Crear ticket
        create_response = self.client.post('/api/v1/tickets',
            data=json.dumps({
                'title': 'Test Ticket',
                'description': 'Esta es una descripción de prueba'
            }),
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        ticket_id = json.loads(create_response.data)['data']['id']
        
        # Actualizar estado
        response = self.client.put(f'/api/v1/tickets/{ticket_id}/status',
            data=json.dumps({'status': 'in_progress'}),
            headers={'Authorization': f'Bearer {token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['status'], 'in_progress')


if __name__ == '__main__':
    unittest.main()
