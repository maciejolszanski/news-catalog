"""
This file contains code to check if website elements are downloadable.
"""

import requests
from bs4 import BeautifulSoup
import string


class WpChecks:
    url = "https://wiadomosci.wp.pl"
    prefixes = string.ascii_lowercase

    def _get_page(self):
        """
        Function returns html content of the page defined in 'url' attribute
        of this class.

        Returns:
            soup (bs4.BeautifulSoup): HTML representation of page defined in
                                      'url' attribute of this class.
        """
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        return soup

    def get_css_prefix(self):
        """
        Function identifies currently used css prefix on page defined as 'url'
        attribute and returns it.

        Returns:
            prefix (str): Currently used css prefix.
        """
        soup = self._get_page()
        for prefix in self.prefixes:
            css_class = prefix + "2PrHTUx"
            results = soup.find_all("div", class_=css_class)

            if len(results) > 0:
                return prefix
