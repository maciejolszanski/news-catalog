import os
import sys

# Add the project root directory to the Python path
cwd = os.getcwd()
root_module_path = os.path.abspath(os.path.join(cwd, "news_catalog"))
sys.path.append(root_module_path)
print(root_module_path)

import pytest
from scrapy_project.scrapy_project.spiders.news_spiders import WPSpider
from scrapy_project.scrapy_project.items import WPArticle
from scrapy.http import HtmlResponse, Request
from scrapy.exceptions import CloseSpider


def test_set_css_classes():
    spider = WPSpider()
    spider.set_css_classes(class_prefix="i")

    assert spider.article_class == "i2PrHTUx"
    assert spider.next_page_class == "i1xRndDA i1ZgYxIQ i2zbd-HY"
    assert spider.article_title_class == "article--title i1xAmRvR"
    assert spider.article_lead_class == "article--lead i1HGmjUl"
    assert spider.article_text_class == "article--text iFQN8OU2 iYwaUr3X"
    assert spider.author_class == "signature--author i2aU53vl desktop"
    assert spider.date_class == "signature--when i2VIX-Kh desktop"


def test_format_date():
    spider = WPSpider()
    formatted_date = spider.format_date("Dzisiaj, 10-02-2024 06:38")

    assert formatted_date == "2024-02-10"


def test_last_scraped_date():
    spider = WPSpider()
    spider.set_last_scraped_date("2024-02-10")

    assert spider.last_scraped_date == "2024-02-10"


def test_extract_html_text_two_xpaths():
    html_response = HtmlResponse(
        url="https://wiadomosci.wp.pl/wiece-w-rosji-zatrzymania-w-moskwie-i-jekaterynburgu-6994208129321536a",
        body='<div class="article--lead c1HGmjUl" data-reactid="322">'
        + "<p>Działacze organizacji Droga do domu...</p></div>",
        encoding="utf-8",
    )

    spider = WPSpider()
    actual_output = spider.extract_html_text(
        html_response,
        css_class="article--lead c1HGmjUl",
        xpath_first_node="div",
        xpath_second_node="p",
    )

    expected_output = "Działacze organizacji Droga do domu..."

    assert actual_output == expected_output


def test_extract_html_text_one_xpath():
    html_response = HtmlResponse(
        url="https://wiadomosci.wp.pl/wiece-w-rosji",
        body='<div class="article--lead c1HGmjUl" data-reactid="322">'
        + "Działacze organizacji Droga do domu...</div>",
        encoding="utf-8",
    )

    spider = WPSpider()
    actual_output = spider.extract_html_text(
        html_response,
        css_class="article--lead c1HGmjUl",
        xpath_first_node="div",
    )

    expected_output = "Działacze organizacji Droga do domu..."

    assert actual_output == expected_output


def test_next_page():
    html_response = HtmlResponse(
        url="https://wiadomosci.wp.pl/",
        body='<a class="c1xRndDA c1ZgYxIQ c2zbd-HY" title="" rel="next" href="/2" data-reactid="1210"></a>',
        encoding="utf-8",
    )

    expected_output = ["https://wiadomosci.wp.pl/2"]

    spider = WPSpider()
    spider.set_css_classes(class_prefix="c")
    actual_output = list(spider._next_page(html_response))

    assert actual_output == expected_output


def test_parse_article_page():
    article_html_body = """
    <h1 class="article--title c1xAmRvR"><!-- react-text: 1758 -->Niech się pan tak nie denerwuje<!-- /react-text --></h1>
    <span class="signature--author c2aU53vl desktop"><!-- react-text: 1751 -->oprac. <!-- /react-text --><!-- react-text: 1752 -->Adam Zygiel<!-- /react-text --></span>
    <div class="signature--when c2VIX-Kh desktop"><span>Dzisiaj, 10-02-2024 16:04</span></div>
    <div class="article--lead c1HGmjUl"><p>Wiceminister rolnictwa napisał.</p></div>
    <div class="article--text cFQN8OU2 cYwaUr3X"><p>Lorem <a href="https://wiadomosci.wp.pl/" rel="seolink">Ipsum.</a></p></div>
    <div class="article--text cFQN8OU2 cYwaUr3X"><p>Lorem</p></div>
    """

    url = "https://wiadomosci.wp.pl/test-article"
    html_response = HtmlResponse(
        url=url, body=article_html_body, encoding="utf-8"
    )

    spider = WPSpider()
    spider.set_css_classes(class_prefix="c")
    spider.set_last_scraped_date("2024-01-01")

    actual_output = list(spider._parse_article_page(html_response, url))[0]

    expected_output = {
        "title": "Niech się pan tak nie denerwuje",
        "date": "2024-02-10",
        "author": "Adam Zygiel",
        "lead": "Wiceminister rolnictwa napisał.",
        "text": "Lorem Ipsum. Lorem",
        "url": url,
    }

    assert isinstance(actual_output, WPArticle)
    assert actual_output == expected_output


def test_parse_article_page_stop_crawling():
    article_html_body = """
    <h1 class="article--title c1xAmRvR"><!-- react-text: 1758 -->Niech się pan tak nie denerwuje<!-- /react-text --></h1>
    <span class="signature--author c2aU53vl desktop"><!-- react-text: 1751 -->oprac. <!-- /react-text --><!-- react-text: 1752 -->Adam Zygiel<!-- /react-text --></span>
    <div class="signature--when c2VIX-Kh desktop"><span>Dzisiaj, 08-02-2024 16:04</span></div>
    <div class="article--lead c1HGmjUl"><p>Wiceminister rolnictwa napisał.</p></div>
    <div class="article--text cFQN8OU2 cYwaUr3X"><p>Lorem <a href="https://wiadomosci.wp.pl/" rel="seolink">Ipsum.</a></p></div>
    <div class="article--text cFQN8OU2 cYwaUr3X"><p>Lorem</p></div>
    """

    url = "https://wiadomosci.wp.pl/test-article"
    html_response = HtmlResponse(
        url=url, body=article_html_body, encoding="utf-8"
    )

    spider = WPSpider()
    spider.set_css_classes(class_prefix="c")
    spider.set_last_scraped_date("2024-02-09")

    with pytest.raises(CloseSpider):
        list(spider._parse_article_page(html_response, url))


def test_parse_articles_listing_articles():
    article_html_body = """
    <a class="c2PrHTUx" title="&quot;Trzeba zrobić w Rosji porządek&quot;. Wałęsa w CNN o historycznej szansie" href="/trzeba-zrobic-w-rosji-porzadek-walesa-w-cnn-o-historycznej-szansie-6994196631181888a" data-reactid="1099"></a>
    <div class="c2eMLotm c2J4C9n0 c2N4iaRc" data-reactid="1121">
    <div class="c2PrHTUx" data-reactid="1122">
    <a class="c2PrHTUx" title="Wiadomo, ile kosztował remont w KGP po granatniku. Wyciekł raport" href="/wiadomo-ile-kosztowal-remont-w-kgp-po-granatniku-wyciekl-raport-6994196319877696a" data-reactid="1123">,</a>
    """

    url = "https://wiadomosci.wp.pl/test-article_list"
    html_response = HtmlResponse(
        url=url, body=article_html_body, encoding="utf-8"
    )

    spider = WPSpider()
    spider.set_css_classes(class_prefix="c")
    spider.set_last_scraped_date("2024-01-01")

    actual_output = list(spider.parse_articles_listing(html_response))

    url_1 = "https://wiadomosci.wp.pl/trzeba-zrobic-w-rosji-porzadek-walesa-w-cnn-o-historycznej-szansie-6994196631181888a"
    url_2 = "https://wiadomosci.wp.pl/wiadomo-ile-kosztowal-remont-w-kgp-po-granatniku-wyciekl-raport-6994196319877696a"

    expected_output = [
        Request(
            url=url_1,
            callback=spider._parse_article_page,
            cb_kwargs={"url": url_1},
        ),
        Request(
            url=url_2,
            callback=spider._parse_article_page,
            cb_kwargs={"url": url_2},
        ),
    ]

    assert isinstance(actual_output[0], Request)
    assert len(actual_output) == 2
    assert actual_output[0].url == expected_output[0].url
    assert actual_output[1].url == expected_output[1].url
    assert actual_output[0].callback == expected_output[0].callback
    assert actual_output[1].callback == expected_output[1].callback
    assert actual_output[0].cb_kwargs == expected_output[0].cb_kwargs
    assert actual_output[1].cb_kwargs == expected_output[1].cb_kwargs


def test_parse_articles_listing_next_page():
    article_html_body = """
    <a class="c2PrHTUx" title="&quot;Trzeba zrobić w Rosji porządek&quot;. Wałęsa w CNN o historycznej szansie" href="/trzeba-zrobic-w-rosji-porzadek-walesa-w-cnn-o-historycznej-szansie-6994196631181888a" data-reactid="1099"></a>
    <div class="c2eMLotm c2J4C9n0 c2N4iaRc" data-reactid="1121">
    <div class="c2PrHTUx" data-reactid="1122">
    <a class="c2PrHTUx" title="Wiadomo, ile kosztował remont w KGP po granatniku. Wyciekł raport" href="/wiadomo-ile-kosztowal-remont-w-kgp-po-granatniku-wyciekl-raport-6994196319877696a" data-reactid="1123">,</a>
    <a class="c1xRndDA c1ZgYxIQ c2zbd-HY" title="" rel="next" href="/2" data-reactid="1220"></a>
    """

    url = "https://wiadomosci.wp.pl/test-article_list"
    html_response = HtmlResponse(
        url=url, body=article_html_body, encoding="utf-8"
    )

    spider = WPSpider()
    spider.set_css_classes(class_prefix="c")
    spider.set_last_scraped_date("2024-01-01")

    actual_output = list(spider.parse_articles_listing(html_response))

    expected_output = [
        Request(
            url="https://wiadomosci.wp.pl/2",
            callback=spider.parse_articles_listing,
        ),
    ]

    assert isinstance(actual_output[-1], Request)
    assert len(actual_output) == 3
    assert actual_output[-1].url == expected_output[-1].url
    assert actual_output[-1].callback == expected_output[-1].callback
