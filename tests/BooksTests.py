import unittest
from request_apis.books_api import BookApi


class BooksTests(unittest.TestCase):

    accessToken = ''

    def setUp(self):
        self.books = BookApi()
        if self.accessToken == '':
            self.accessToken = self.books.post_api_clients().json()['accessToken']

    # this tests will check the status code and body for
    # /status endpoint
    def test_books_status(self):
        response = self.books.get_api_status_response()
        self.assertEqual(200,response.status_code, "Status code is not the same: ")
        self.assertEqual(response.json()['status'], "OK", "GET /status response value for key 'status' is not the same: ")

    def tests_all_books(self):
        response = self.books.get_api_books_response()
        self.assertEqual(200,response.status_code,"Status code is not the same: ")

        expected_number = 6
        self.assertEqual(len(response.json()), expected_number, "GET /books length is not the same: ")
        self.assertEqual(response.json()[0]['id'], 1, "Id for the first book is not the same: ")

        #for book in response.json():
            #self.assertEqual(len(response.json()), expected_number, "GET /books length is not the same: ")

        # TODO use for book in response.json() and check every fields received

    def test_book_by_id(self):
        response = self.books.get_api_books_book_by_id(1)
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        self.assertEqual(response.json()['name'], "The Russian", "GET /books/{id} response value for key 'name' is not the same: ")

    def test_book_by_id_negative(self):
        non_existing_id = 100
        response = self.books.get_api_books_book_by_id(non_existing_id)
        self.assertEqual(404,response.status_code, "Status code is not the same: ")
        self.assertEqual(response.json()['error'], f"No book with id {non_existing_id}", "GET /books/{id} response for key 'error' is not the same: ")


    def test_book_orders_no_token(self):
        response = self.books.get_api_orders_response('213')
        self.assertEqual(401, response.status_code, "Status code is not the same")

    def test_all_orders(self):
        response = self.books.get_api_orders_response(self.accessToken)
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        # de verificat la fel ca la books all

    def test_post_orders(self):
        book_id = 1
        customer_name = "Augustin_Balan"
        response = self.books.post_books_order(self.accessToken, book_id, customer_name)
        self.assertEqual(201, response.status_code, "Status code is not the same: ")

    def test_post_orders_flow(self):
        book_id = 1
        customer_name = "Augustin_Balan"
        response = self.books.post_books_order(self.accessToken, book_id, customer_name)
        self.assertEqual(201, response.status_code, "Status code is not the same: ")

        # now we check that we have one order
        response = self.books.get_api_orders_response(self.accessToken)
        self.assertEqual(200, response.status_code, "Status code is not the same: ")

        expected_number = 1
        self.assertEqual(len(response.json()), expected_number, "GET /orders length is not the same: ")

    def test_patch_order_flow(self):
        book_id = 1
        customer_name = "Augustin_Balan"
        response = self.books.post_books_order(self.accessToken, book_id, customer_name)
        self.assertEqual(201, response.status_code,"Status code is not the same: ")

        order_id = response.json()['orderId']
        new_customer_name = "Augustin_Balan2"
        response = self.books.patch_books_order(self.accessToken, order_id, new_customer_name)
        self.assertEqual(204, response.status_code, "PATCH /orders/{id} status code is not the same: ")
        #todo make another GET /orders request and check if the new value is set for customer name