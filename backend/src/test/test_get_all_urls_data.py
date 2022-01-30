def test_setup_module(test_app):
    url_data = {"url_data": {
        "url": "https://www.google.com/",
        "user_short_link": "my link"
    }
    }
    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 201, 'Setup module failed!'

    url_data = {"url_data": {
        "url": "https://www.ya.ru/",
        "user_short_link": "my super link"
    }
    }
    response = test_app.post('/shorten/', json=url_data)
    assert response.status_code == 201, 'Setup module failed!'


def test_get_all_url_data(test_app):
    response_json = [
        {
            "url": "https://www.google.com/",
            "user_short_link": "my link",
            "id": 1,
            "short link": "$b",
            "url_hash": "8ffdefbdec956b595d257f0aaeefd623",
            "user_link_hash": "3550fbbf04"
        },
        {
            "url": "https://www.ya.ru/",
            "user_short_link": "my super link",
            "id": 2,
            "short link": "$c",
            "url_hash": "9b3e9f01e78910b0a714628ccf609937",
            "user_link_hash": "d3e68027d6"
        }
    ]

    response = test_app.get('/shorten/', params={'skip': 0, 'limit': 100})
    assert response.status_code == 200
    answer = response.json()
    for url in answer:
        assert url.pop('created_at') is not None
    assert answer == response_json



