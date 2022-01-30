def test_setup_module(test_app):
    url_data = {"url_data": {
        "url": "https://www.google.com/",
        "user_short_link": "my link"
    }
    }
    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 201, 'Error setup module!'


def test_edit_not_exists_url(test_app):
    response_json = {
        "detail": "Not Found"
    }
    edit_data = {
        "url_data": {
            "url": "https://www.google.com/",
            "user_short_link": "my super link"
        }
    }
    response = test_app.put('/shorten/url_data/2/', json=edit_data)
    assert response.status_code == 404
    assert response.json() == response_json


def test_edit_url(test_app):
    edit_data = {
        "url_data": {
            "url": "https://www.google.com/",
            "user_short_link": "my super link"
        }
    }
    response_json = {
        "url": "https://www.google.com/",
        "user_short_link": "my super link",
        "id": 1,
        "short link": "$b",
        "url_hash": "8ffdefbdec956b595d257f0aaeefd623",
        "user_link_hash": "d3e68027d6"
    }

    response = test_app.put('/shorten/url_data/1/', json=edit_data)
    assert response.status_code == 200
    answer = response.json()
    assert answer.pop('created_at') is not None
    assert answer == response_json
