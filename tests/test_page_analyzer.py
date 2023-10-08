import pytest
from page_analyzer.app import create_app
from page_analyzer.utils import normalize_url
from tests.utils import get_fixture_content


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert "Анализатор страниц" in response.text
    assert "Сайты" in response.text


@pytest.mark.parametrize('urls_json',
                         [pytest.param('wrong_urls.json')])
def test_wrong_urls(client, urls_json):
    for url in get_fixture_content(urls_json):
        response = client.post('/urls', data={'url': url},
                               follow_redirects=True)

        assert "Некорректный URL" in response.text
        assert response.status_code == 422


@pytest.mark.parametrize('urls_json',
                         [pytest.param('correct_urls.json')])
def test_correct_urls(client, urls_json):
    for url in get_fixture_content(urls_json):
        response = client.post('/urls', data={'url': url},
                               follow_redirects=True)

        assert "Некорректный URL" not in response.text
        assert response.status_code == 200

    check_response = client.post('/urls/1/checks', data={'url': url},
                                 follow_redirects=True)

    assert check_response.status_code == 200
    assert "<td>200</td>" in check_response.text


@pytest.mark.parametrize('urls_json',
                         [pytest.param('correct_urls.json')])
def test_list_request(client, urls_json):
    urls = [url for url in get_fixture_content(urls_json)]
    for url in urls:
        client.post('/urls', data={'url': url},
                    follow_redirects=True)

    list_response = client.get('/urls')
    for url in [normalize_url(url) for url in urls]:
        assert url in list_response.text
