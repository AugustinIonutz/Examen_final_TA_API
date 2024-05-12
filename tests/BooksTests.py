import unittest
from request_apis.books_api import BookApi


class BooksTests(unittest.TestCase):

    accessToken = ''

    # we need to replicate the response from database
    # because we don't have access to API database we mock the response from DB and use it
    # in our tests
    books_from_db = [
        {
            "id": 1,
            "name": "The Russian",
            "type": "fiction",
            "available": True
        },
        {
            "id": 2,
            "name": "Just as I Am",
            "type": "non-fiction",
            "available": False
        },
        {
            "id": 3,
            "name": "The Vanishing Half",
            "type": "fiction",
            "available": True
        },
        {
            "id": 4,
            "name": "The Midnight Library",
            "type": "fiction",
            "available": True
        },
        {
            "id": 5,
            "name": "Untamed",
            "type": "non-fiction",
            "available": True
        },
        {
            "id": 6,
            "name": "Viscount Who Loved Me",
            "type": "fiction",
            "available": True
        }
    ]
    # Here we set up the tests suite
    def setUp(self):
        self.books = BookApi()
        if self.accessToken == '':
            self.accessToken = self.books.post_api_clients().json()['accessToken']

    # this test will check the status code and body for
    # /status endpoint
    def test_get_books_status(self):
        response = self.books.get_api_status_response()
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        self.assertEqual(response.json()['status'], "OK", "GET /status response value for key 'status' is not the same: ")

    # this test will check the status code and body for
    # /books endpoint
    def tests_get_all_books(self):
        response = self.books.get_api_books_response()
        self.assertEqual(200, response.status_code, "Status code is not the same: ")

        expected_number = 6
        self.assertEqual(len(response.json()), expected_number, "GET /books length is not the same: ")
        self.assertEqual(response.json()[0]['id'], 1, "Id for the first book is not the same: ")

    # this test will check the status code and body using a for loop
    def test_get_all_books_loop(self):
        response = self.books.get_api_books_response()
        self.assertEqual(response.status_code, 200, "Status code is not the same: ")

        books_from_api = response.json()

        self.assertEqual(len(books_from_api), len(self.books_from_db), "Number of books is not the same: ")

        for index in range(0, len(books_from_api)):
            book = books_from_api[index]
            self.assertEqual(book['id'], self.books_from_db[index]["id"], "Id of the book is not the same: ")
            self.assertEqual(book['name'], self.books_from_db[index]["name"], "Name of the book is not the same: ")
            self.assertEqual(book['type'], self.books_from_db[index]["type"], "Type of the book is not the same: ")
            self.assertEqual(book['available'], self.books_from_db[index]["available"], "Availability of the book is not the same: ")

    # this test will check the status code and body for /books/:bookId endpoint
    # "id": 1
    def test_get_book_by_id(self):
        response = self.books.get_api_books_book_by_id(1)
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        self.assertEqual(response.json()['name'], "The Russian", "GET /books/{id} response value for key 'name' is not the same: ")
        self.assertEqual(response.json()['author'], "James Patterson and James O. Born", "Name of the author is not the same: ")
        self.assertEqual(response.json()['isbn'], "1780899475", "ISBN number is not the same: ")
        self.assertEqual(response.json()['available'], True, "Availability of the book is not the same: ")
        self.assertEqual(response.json()['type'], "fiction", "Type of the book is not the same: ")

    # this test will check the status code and body for /books/:bookId endpoint
    # using a non-existing id
    def test_get_book_by_id_negative(self):
        non_existing_id = 100
        response = self.books.get_api_books_book_by_id(non_existing_id)
        self.assertEqual(404, response.status_code, "Status code is not the same: ")
        self.assertEqual(response.json()['error'], f"No book with id {non_existing_id}", "GET /books/{id} response for key 'error' is not the same: ")

    # this test will check the status code and length for the /books& limit parameter endpoint
    # with limit = 2
    def test_get_all_books_filter_by_limit(self):
        response = self.books.get_books_by_filters(limit=2)
        expected_number = 2
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        self.assertEqual(len(response.json()), expected_number, "Number of books is not the same: ")

    # this test will check that we cannot get a book by an invalid parameter
    # (invalid_limit=21)
    def test_get_all_books_filter_by_limit_negative(self):
        response = self.books.get_books_by_filters(limit=21)
        expected_error_message = "Invalid value for query parameter 'limit'. Cannot be greater than 20."
        actual_response_message = response.json()['error']
        self.assertEqual(400, response.status_code, "Status code is not the same: ")
        self.assertEqual(expected_error_message, actual_response_message, "Error message is not the same: ")

    # this test will check that we cannot get a book by an invalid parameter
    # (invalid_value_limit=-1)
    def test_get_all_books_filter_by_limit_negative_number(self):
        response = self.books.get_books_by_filters(limit=-1)
        expected_error_message = "Invalid value for query parameter 'limit'. Must be greater than 0."
        actual_response_message = response.json()['error']
        self.assertEqual(400, response.status_code, "Status code is not the same: ")
        self.assertEqual(expected_error_message, actual_response_message, "Error message is not the same: ")

    # this test will check the status code and length for the /books& book_type parameter endpoint
    # with book_type = "fiction"
    def test_get_all_books_filter_by_type_fiction(self):
        response = self.books.get_books_by_filters(book_type="fiction")
        expected_number = 4
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        self.assertEqual(len(response.json()), expected_number, "Number of books is not the same: ")

    # this test will check the status code and length for the /books& book_type parameter endpoint
    # with book_type = "non-fiction"
    def test_get_all_books_filter_by_type_nonfiction(self):
        response = self.books.get_books_by_filters(book_type="non-fiction")
        expected_number = 2
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        self.assertEqual(len(response.json()), expected_number, "Number of books is not the same: ")

    # this test will check that we cannot get a book by an invalid parameter
    # (invalid_value_type="crime")
    def test_get_all_books_filter_by_type_negative(self):
        response = self.books.get_books_by_filters(book_type="crime")
        expected_error_message = "Invalid value for query parameter 'type'. Must be one of: fiction, non-fiction."
        actual_error_message = response.json()['error']
        self.assertEqual(400, response.status_code, "Status code is not the same: ")
        self.assertEqual(expected_error_message, actual_error_message, "Error message is not the same: ")

    # this test will check that we cannot make an order without a valid token
    def test_get_book_orders_no_token(self):
        response = self.books.get_api_orders_response('213')
        self.assertEqual(401, response.status_code, "Status code is not the same: ")

    # this test will check the status code and body for /orders endpoint
    def test_get_all_orders(self):
        response = self.books.get_api_orders_response(self.accessToken)
        self.assertEqual(200, response.status_code, "Status code is not the same: ")
        expected_number = 0
        self.assertEqual(len(response.json()), expected_number, "Number of orders is not the same: ")

    # this test will check that we cannot see an order with an invalid order id
    def test_get_books_order_by_id_negative(self):
        invalid_order_id = "InvalidOrderId"
        response = self.books.get_api_orders_by_id_response(self.accessToken, invalid_order_id)
        self.assertEqual(response.status_code, 404, "Status code is not the same")
        self.assertEqual(response.json()['error'], f"No order with id {invalid_order_id}.", "Error message is not the same")

    # This test will check if we can order a book
    def test_post_orders(self):
        book_id = 1
        customer_name = "Augustin_Balan"
        response = self.books.post_books_order(self.accessToken, book_id, customer_name)
        self.assertEqual(201, response.status_code, "Status code is not the same: ")

    # this test will check if we can order a book and that we have an order
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

    # The request body for the following test needs to be in JSON format and include the following properties:
    # bookId - Integer - Required
    # customerName - String - Required
    def test_post_orders_negative_BUG(self):  # BUG FOUND
        book_id = "1"  # the value for key "book_id" must be Integer
        customer_name = "Augustin_Balan"
        response = self.books.post_books_order(self.accessToken, book_id, customer_name)
        self.assertEqual(400, response.status_code, "Status code is not the same: ")

        expected_error_message = "Invalid or missing bookId."
        actual_message = response.json()  # Actual message is 'created': True, 'orderId': '....'
        self.assertEqual(expected_error_message, actual_message, "Error message is not the same: ")

    # This test will check if we can update the customer name of an existing order
    def test_patch_order_flow(self):
        book_id = 1
        customer_name = "Augustin_Balan"
        response = self.books.post_books_order(self.accessToken, book_id, customer_name)
        self.assertEqual(201, response.status_code, "Status code is not the same: ")

        order_id = response.json()['orderId']
        new_customer_name = "Augustin_Balan2"
        response = self.books.patch_books_order(self.accessToken, order_id, new_customer_name)
        self.assertEqual(204, response.status_code, "PATCH /orders/{id} status code is not the same: ")

        # this part of the test will check if the new value is set for customer name label
        response = self.books.get_api_orders_by_id_response(self.accessToken, order_id)
        self.assertEqual(response.json()['customerName'], "Augustin_Balan2", "GET //orders/{id} response value for key 'customerName' is not the same: ")

    # this test will check that we cannot delete an order without a valid order id
    def test_delete_invalid_order(self):
        invalid_order_id = "InvalidOrderId"
        response = self.books.delete_books_order(self.accessToken, invalid_order_id)
        self.assertEqual(response.status_code, 404, "Status code is not the same")
        self.assertEqual(response.json()['error'], f"No order with id {invalid_order_id}.", "Error message is not the same")

    # this test will check if we can delete an existing order
    def test_delete_valid_order(self):
        response = self.books.get_api_books_response()
        self.assertEqual(response.status_code, 200, "Status code is not the same")

        # this part of the test creates an order
        random_book_id = response.json()[0]["id"]
        response = self.books.post_books_order(self.accessToken, random_book_id, "Augustin")

        # this part of the test removes the order created above
        order_id = response.json()["orderId"]
        response = self.books.delete_books_order(self.accessToken, order_id)
        self.assertEqual(response.status_code, 204, "Status code is not the same")

        # this part of the test checks if the order was successfully removed
        response = self.books.get_api_orders_by_id_response(self.accessToken, order_id)
        self.assertEqual(response.status_code, 404, "Status code is not the same")
        self.assertEqual(response.json()["error"], f"No order with id {order_id}.", "Error message is not the same")
