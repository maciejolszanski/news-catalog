import sys
import os

# Add the project root directory to the Python path
cwd = os.getcwd()
root_module_path = os.path.abspath(os.path.join(cwd, os.pardir))
sys.path.append(root_module_path)

import pytest
from bs4 import BeautifulSoup
from website_connection_checks import WpChecks


@pytest.fixture
def hardcoded_soup_content():
    # Hardcoded HTML content for testing
    html_content = """
    <html>
        <body>
            <div class="a2PrHTUx">Test</div>
        </body>
    </html>
    """
    return BeautifulSoup(html_content, "html.parser")


def test_get_css_prefix_with_hardcoded_soup(
    monkeypatch, hardcoded_soup_content
):
    def mock_get_page(self):
        return hardcoded_soup_content

    monkeypatch.setattr(WpChecks, "_get_page", mock_get_page)

    wp_checks_instance = WpChecks()
    result = wp_checks_instance.get_css_prefix()

    assert result == "a"
