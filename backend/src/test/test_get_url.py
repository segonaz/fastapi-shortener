def test_setup_module(test_app):
    url_data = {"url_data": {
        "url": "https://www.google.com/",
        "user_short_link": "my link"
    }
    }
    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 201, 'Setup module failed!'


def test_get_url_by_user_short_link_not_exists(test_app):
    response_json = {
        "detail": "Not Found"
    }

    response = test_app.get('/shorten/user wrong link/')
    assert response.status_code == 404
    assert response.json() == response_json


def test_get_url_by_user_short_link(test_app):

    url = 'https://www.google.com/'
    response = test_app.get('/shorten/my link')
    answer = response.history[1]
    assert answer.status_code == 301
    assert answer.headers['location'] == url


def test_get_url_by_short_link(test_app):

    url = 'https://www.google.com/'
    response = test_app.get('/shorten/$b')
    answer = response.history[1]
    assert answer.status_code == 301
    assert answer.headers['location'] == url

