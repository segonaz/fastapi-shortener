def test_setup_module(test_app):
    url_data = {"url_data": {
        "url": "https://www.google.com/",
        "user_short_link": "my link"
    }
    }
    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 201, 'Setup module failed!'


def test_get_url_data_by_user_short_link_not_exists(test_app):
    response_json = {
        "detail": "Not Found"
    }

    response = test_app.get('/shorten/url_data/', params={'short_link': 'my wrong link'})
    assert response.status_code == 404
    assert response.json() == response_json


def test_get_url_data_by_user_short_link(test_app):

    response_json = {
      "url": "https://www.google.com/",
      "user_short_link": "my link",
      "id": 1,
      "short link": "$b",
      "url_hash": "8ffdefbdec956b595d257f0aaeefd623",
      "user_link_hash": "3550fbbf04"
    }
    response = test_app.get('/shorten/url_data/', params={'short_link': 'my link'})
    assert response.status_code == 200
    answer = response.json()
    assert answer.pop('created_at') is not None
    assert answer == response_json


def test_get_url_by_short_link(test_app):
    response_json = {
        "url": "https://www.google.com/",
        "user_short_link": "my link",
        "id": 1,
        "short link": "$b",
        "url_hash": "8ffdefbdec956b595d257f0aaeefd623",
        "user_link_hash": "3550fbbf04"
    }
    response = test_app.get('/shorten/url_data/', params={'short_link': '$b'})
    assert response.status_code == 200
    answer = response.json()
    assert answer.pop('created_at') is not None
    assert answer == response_json
