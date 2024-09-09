import pytest
import requests

API_URL = "https://qa-internship.avito.com/api/1"
CREATE_ITEM_STATUS_PREFIX = r"Сохранили объявление - "


def extract_item_id(status):
    if status.startswith(CREATE_ITEM_STATUS_PREFIX):
        return status[len(CREATE_ITEM_STATUS_PREFIX):]
    return None


@pytest.mark.parametrize("payload, expected_response_status_code", [
    # TC-1. Введение корректных значений в Body
    pytest.param(
        {
            "name": "Телефон",
            "price": 777,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 200, id="TC-1"),
    # TC-2: Введение в поле "name" чисел
    pytest.param(
        {
            "name": 897,
            "price": 777,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-2"),
    # TC-3: Введение в поле "name" пустого значения
    pytest.param(
        {
            "name": "",
            "price": 777,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-3"),
    # TC-4: Введение в поле "name" значения null
    pytest.param(
        {
            "name": None,
            "price": 777,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-4"),
    # TC-5: Введение в поле "name" большого значения
    pytest.param(
        {
            "name": "Телефонелефонелефонелефонелефонелефонелефон",
            "price": 777,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-5"),
    # TC-6: Введение в поле "price" большого значения
    pytest.param(
        {
            "name": "Телефон",
            "price": 777777777777777777777777777777777777777777,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-6"),
    # TC-7: Введение в поле "price" значения null
    pytest.param(
        {
            "name": "Телефон",
            "price": None,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-7"),
    # TC-8: Введение в поле "price" значения "Семьсот рублей"
    pytest.param(
        {
            "name": "Телефон",
            "price": "Семьсот рублей",
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-8"),
    # TC-9: Введение в поле "price" значения 0
    pytest.param(
        {
            "name": "Телефон",
            "price": 0,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 200, id="TC-9"),
    # TC-10: Введение в поле "sellerId" значения внутри класса
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 199496,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 200, id="TC-10"),
    # TC-11: Введение в поле "sellerId" значения на нижней границе класса
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 111111,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 200, id="TC-11"),
    # TC-12: Введение в поле "sellerId" значения на верхней границе класса
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 999999,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 200, id="TC-12"),
    # TC-13: Введение в поле "sellerId" значения вне класса снизу
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 111110,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-13"),
    # TC-14: Введение в поле "sellerId" значения null
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": None,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-14"),
    # TC-15: Введение в поле "sellerId" значения вне класса сверху
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 1000000,
            "statistics": {
                "contacts": 32,
                "like": 35,
                "viewCount": 14
            }
        }, 400, id="TC-14"),
    # TC-16: Введение в поля "statistics" значения null
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 567890,
            "statistics": {
                "contacts": None,
                "like": None,
                "viewCount": None
            }
        }, 400, id="TC-16"),
    # TC-17: Введение в поля "statistics" отрицательного значения
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 567890,
            "statistics": {
                "contacts": -17,
                "like": -17,
                "viewCount": -17
            }
        }, 400, id="TC-17"),
    # TC-18: Введение в поля "statistics" больших значений
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 567890,
            "statistics": {
                "contacts": 78900086544,
                "like": 777777777777,
                "viewCount": 9999999999999
            }
        }, 400, id="TC-18"),
    # TC-19: Введение в Body пустой JSON
    pytest.param({}, 400, id="TC-19"),
    # TC-20: Введение запроса с пустым Body
    pytest.param(None, 400, id="TC-20"),
    # TC-21: Отсутствие поля "name"
    pytest.param(
        {
            "price": 700,
            "sellerId": 567890,
            "statistics": {
                "contacts": 10,
                "like": 10,
                "viewCount": 19
            }
        }, 400, id="TC-21"),
    # TC-22: Отсутствие поля "price"
    pytest.param(
        {
            "name": "Телефон",
            "sellerId": 567890,
            "statistics": {
                "contacts": 78900086544,
                "like": 777777777777,
                "viewCount": 9999999999999
            }
        }, 400, id="TC-22"),
    # TC-23: Отсутствие поля "sellerId"
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "statistics": {
                "contacts": 78900086544,
                "like": 777777777777,
                "viewCount": 9999999999999
            }
        }, 400, id="TC-23"),
    # TC-24: Отсутствие полей "statistics"
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 567890,
            "statistics": {
            }
        }, 400, id="TC-24"),
    # TC-25: Отсутствие поля "statistics"
    pytest.param(
        {
            "name": "Телефон",
            "price": 700,
            "sellerId": 567890,
        }, 400, id="TC-25"),
])
def test_create_item(payload, expected_response_status_code):
    response = requests.post(f"{API_URL}/item", json=payload)
    assert response.status_code == expected_response_status_code
    if response.status_code == 200:
        response_json = response.json()
        status = response_json["status"]
        item_id = extract_item_id(status)
        assert len(item_id) > 0


# TC-26: Введение некорректного метода
@pytest.mark.parametrize("", [pytest.param(id="TC-26")])
def test_create_item_incorrect_method():
    payload = {
        "name": "Телефон",
        "sellerId": 567890,
        "statistics": {
            "contacts": 78900086544,
            "like": 777777777777,
            "viewCount": 9999999999999
        }
    }
    response = requests.put(f"{API_URL}/item", json=payload)
    assert response.status_code == 405


# TC-27: Введение корректного идентификатора
@pytest.mark.parametrize("", [pytest.param(id="TC-27")])
def test_get_item_by_correct_id():
    payload = {
        "name": "Телефон",
        "price": 777,
        "sellerId": 199496,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    create_item_response = requests.post(f"{API_URL}/item", json=payload)
    create_item_response_json = create_item_response.json()
    status = create_item_response_json["status"]
    item_id = extract_item_id(status)
    get_item_response = requests.get(f"{API_URL}/item/{item_id}")
    assert get_item_response.status_code == 200
    get_item_response_json = get_item_response.json()
    assert len(get_item_response_json) == 1
    response_item = get_item_response_json[0]
    assert response_item["id"] == item_id
    assert response_item["name"] == payload["name"]
    assert response_item["price"] == payload["price"]
    assert response_item["sellerId"] == payload["sellerId"]
    assert response_item["statistics"] == payload["statistics"]


@pytest.mark.parametrize("item_id", [
    pytest.param("abcde", id="TC-28"),  # TC-28: Введение некорректного идентификатора
    pytest.param("", id="TC-29"),  # TC-29: Введение пустого идентификатора
])
def test_get_item_by_incorrect_id(item_id):
    response = requests.get(f"{API_URL}/item/{item_id}")
    assert response.status_code == 400 or response.status_code == 404


# TC-30: Введение корректного id продавца
@pytest.mark.parametrize("", [pytest.param(id="TC-30")])
def test_get_items_by_correct_seller_id():
    seller_id = 199496
    payload = {
        "name": "Телефон",
        "price": 777,
        "sellerId": seller_id,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    create_item_response = requests.post(f"{API_URL}/item", json=payload)
    create_item_response_json = create_item_response.json()
    status = create_item_response_json["status"]
    item_id = extract_item_id(status)
    get_items_response = requests.get(f"{API_URL}/{seller_id}/item")
    assert get_items_response.status_code == 200
    get_items_response_json = get_items_response.json()
    for item in get_items_response_json:
        if item["id"] == item_id:
            return
    assert False


# TC-31: Введение некорректного id продавца
@pytest.mark.parametrize("", [pytest.param(id="TC-31")])
def test_get_items_by_incorrect_seller_id():
    get_items_response = requests.get(f"{API_URL}/1234/item")
    assert get_items_response.status_code == 200
    get_items_response_json = get_items_response.json()
    assert len(get_items_response_json) == 0


# TC-32: Введение пустого id продавца
@pytest.mark.parametrize("", [pytest.param(id="TC-32")])
def test_get_items_by_empty_seller_id():
    get_items_response = requests.get(f"{API_URL}//item")
    assert get_items_response.status_code == 400 or get_items_response.status_code == 404


# TC-33: Введение другого id продавца
@pytest.mark.parametrize("", [pytest.param(id="TC-33")])
def test_get_items_by_another_seller_id():
    payload = {
        "name": "Телефон",
        "price": 777,
        "sellerId": 199496,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    create_item_response = requests.post(f"{API_URL}/item", json=payload)
    create_item_response_json = create_item_response.json()
    status = create_item_response_json["status"]
    item_id = extract_item_id(status)
    get_items_response = requests.get(f"{API_URL}/199497/item")
    assert get_items_response.status_code == 200
    get_items_response_json = get_items_response.json()
    for item in get_items_response_json:
        if item["id"] == item_id:
            assert False
