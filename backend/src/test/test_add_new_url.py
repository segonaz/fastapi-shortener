def test_add_new_url(test_app):
    url_data = {"url_data": {
        "url": "https://www.google.com/",
        "user_short_link": "my link"
    }
    }
    response_json = {
        'url': 'https://www.google.com/',
        'user_short_link': 'my link',
        'id': 1,
        'short link': '$b',
        'url_hash': '8ffdefbdec956b595d257f0aaeefd623',
        'user_link_hash': '3550fbbf04'
    }

    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 201
    answer = response.json()
    assert answer.pop('created_at') is not None
    assert answer == response_json


def test_add_new_exists_url(test_app):
    url_data = {"url_data": {
        "url": "https://www.google.com/",
        "user_short_link": "my link"
    }
    }
    response_json = {
        "detail": "Url already exist"
    }

    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 400
    assert response.json() == response_json


def test_add_new_exists_short_link(test_app):
    url_data = {"url_data": {
        "url": "https://www.ya.ru/",
        "user_short_link": "my link"
    }
    }
    response_json = {
        "detail": "User short link already exist"
    }

    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 400
    assert response_json == response.json()
