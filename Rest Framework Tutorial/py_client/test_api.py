import requests


def test_get_detail_view():
    endpoint = "http://localhost:8000/api/products/1/"
    response = requests.get(endpoint)
    print(response.json())


def test_get_list_view():
    endpoint = "http://localhost:8000/api/products/"
    response = requests.get(endpoint)
    for item in response.json():
        print(item, '\n')


def test_create_item_view():
    endpoint = "http://localhost:8000/api/products/"
    response = requests.post(
        endpoint,
        json={
            "title": "testing fbv 101",
            "price": 499,
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
    endpoint = "http://localhost:8000/api/products/9/delete/"
    response = requests.delete(endpoint)
    print(response.status_code)


test_get_list_view()
# test_get_detail_view()
# test_create_item_view()
# test_abnormal_view()
# test_update_view()
# test_delete_view()
