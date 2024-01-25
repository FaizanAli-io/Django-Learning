import requests


def get_auth_token():
    endpoint = "http://localhost:8000/api/auth/"
    data = {'username': 'faizanali', 'password': 'hello'}
    token = requests.post(endpoint, json=data).json()['token']
    return {"Authorization": f"Bearer {token}"}


def test_get_detail_view():
    endpoint = "http://localhost:8000/api/products/1/"
    response = requests.get(endpoint)
    print(response.json())


def test_get_list_view():
    endpoint = "http://localhost:8000/api/products/"
    auth_header = get_auth_token()
    print(auth_header)

    response = requests.get(endpoint, headers=auth_header)

    for item in response.json():
        print(item, '\n')


def test_create_item_view():
    endpoint = "http://localhost:8000/api/products/"
    response = requests.post(
        endpoint,
        json={
            "title": "damn ok",
            "content": "lalalalala",
            "price": 1.99,
        },
    )
    print(response.json())


def test_abnormal_view():
    endpoint = "http://localhost:8000/api/products/10000"
    response = requests.get(endpoint)
    print(response.json())


def test_update_view():
    endpoint = "http://localhost:8000/api/products/1/update/"
    response = requests.put(
        endpoint,
        json={
            "title": "Hello darkness my old friend",
            "price": 123.45,
        },
    )
    print(response.json())


def test_delete_view():
    id = int(input('ID you want to delete: '))
    endpoint = f"http://localhost:8000/api/products/{id}/delete/"
    response = requests.delete(endpoint)
    print(response.status_code)


def clean_database():
    endpoint = "http://localhost:8000/api/products/clean/"
    response = requests.get(endpoint)
    print(response.status_code)


# get_auth_token()

# test_get_list_view()
# test_get_detail_view()
# test_create_item_view()
# test_abnormal_view()
# test_update_view()
# test_delete_view()

# clean_database()
