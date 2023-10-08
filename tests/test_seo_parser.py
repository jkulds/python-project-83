import pytest

from page_analyzer.seo_parser import get_seo_info_dict
from tests.utils import get_fixture_content


@pytest.mark.parametrize("html_path, result_path",
                         [pytest.param('seo_in.html', 'seo_out.json')])
def test_get_seo_info_from_html(html_path: str, result_path: str):
    html = get_fixture_content(html_path)
    actual = get_seo_info_dict(html)
    expected = get_fixture_content(result_path)

    assert actual == expected
