def test_setup_module(test_app):
    url_data = {"url_data": {
        "url": "https://www.google.com/",
        "user_short_link": "my link"
    }
    }
    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 201, 'Error setup module!'


def test_delete_not_exists_url(test_app):

    response_json = {
        "detail": "Not Found"
    }

    response = test_app.delete('/shorten/url_data/2/')
    assert response.status_code == 404
    assert response.json() == response_json


def test_delete_url(test_app):

    response = test_app.delete('/shorten/url_data/1/')
    assert response.status_code == 204
    assert response.text == ''
