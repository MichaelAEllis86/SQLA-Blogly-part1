from unittest import TestCase
from app import app
from flask import request

class FlaskTests(TestCase):

    def setUp(self):
        """setup! enabling flask testing configs here and getting rid of DB TB during testing"""
        app.config['TESTING']=True
        app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']

        class FlaskTests(TestCase):
    
    def test_root_page(self):
        """Test if root page returns correct status code for GET request and returns included html"""
        with app.test_client() as client:
            response=client.get("/")
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1 id="basewelcome">  Welcome to Forex! &#128123 Happy Halloween! &#127875</h1>',html)
    
    def test_converter_form_page(self):
        """Test if converter form page returns correct status code for GET request and returns included html"""
        with app.test_client() as client:
            response=client.get("/converterform")
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1 id="convertpagewelcome">Welcome to the Converter Page</h1>',html)
    
    def test_converter_submit_redirect(self):
        """Test if converter form page submit returns correct status code for redirect and redirects to correct location"""
        with app.test_client() as client:
            response=client.post("convertform/send", data={'converting-from':'USD', 'converting-to':'USD','amount':'1'})
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,302)
            self.assertIn(response.location,"/converterform")
    
    def test_converter_submit_redirect_html(self):
        """Test if converter form page submit returns correct status code and html after full redirect and proper flash message response"""
        with app.test_client() as client:
            response=client.post("convertform/send",follow_redirects=True ,data={'converting-from':'USD', 'converting-to':'USD','amount':'1'})
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1 id="convertpagewelcome">Welcome to the Converter Page</h1>',html)
            self.assertIn('<p class="success">success Your conversion is $1.00</p>',html)
