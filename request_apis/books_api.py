import requests
import random

class BookApi:

    _BASE_URL = "https://simple-books-api.glitch.me"
    _STATUS_ENDPOINT = "/status"
    _BOOKS_ENDPOINT = "/books"
    _ORDERS_ENDPOINT = "/orders"
    _API_CLIENTS_ENDPOINT = "/api-clients"

    def _get_status_route(self):
        return self._BASE_URL + self._STATUS_ENDPOINT

    def _get_books_route(self):
        return self._BASE_URL + self._BOOKS_ENDPOINT

    def _get_book_by_id_route(self, book_id):
        return self._get_books_route() + f'/{book_id}'

    def _get_orders_route(self):
        return self._BASE_URL + self._ORDERS_ENDPOINT

    def _get_order_by_id_route(self, order_id):
        return self._get_orders_route() + f'/{order_id}'

    def _get_api_clients_route(self):
        return self._BASE_URL + self._API_CLIENTS_ENDPOINT

    def get_api_status_response(self):
        URL = self._get_status_route()
        return requests.get(url=URL)

    def get_api_books_response(self):
        URL = self._get_books_route()
        return requests.get(url=URL)

    def get_api_books_book_by_id(self, book_id):
        URL = self._get_book_by_id_route(book_id)
        return requests.get(url=URL)

    def get_api_books_by_filters(self, limit, book_type):
        URL = self._get_books_route()

        query_params = {
            "limit": limit,
            "type": book_type
        }

        return requests.get(url=URL, params=query_params)

    def get_api_orders_response(self, access_token):
        URL = self._get_orders_route()

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        return requests.get(url=URL, headers=headers)

    def post_api_clients(self):
        URL = self._get_api_clients_route()
        random_number = random.randint(1, 9999999999999999)

        body = {
            "clientName": "Augustin_Balan",
            "clientEmail": f"emailaddress{random_number}@gmail.com"
        }

        return requests.post(url=URL, json=body)

    def post_books_order(self, access_token, book_id, customer_name):
        URL = self._get_orders_route()

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        body = {
            "bookId": book_id,
            "customerName": customer_name
        }

        return requests.post(url=URL, json=body, headers=headers)

    def patch_books_order(self, access_token, order_id, customer_name):
        URL = self._get_order_by_id_route(order_id)

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        body = {
            "customerName": customer_name
        }

        return requests.patch(url=URL, json=body, headers=headers)



