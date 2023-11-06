from pathlib import Path

import scrapy


class WPSpider(scrapy.Spider):
    
    name = "wp_spider"

    
    def start_requests(self):
        """This is a function that runs after calling a spider

        Raises:
            AttributeError: Raised if there is no CSS classes prefix defined
                            during spider call.
        """
        url = "https://wiadomosci.wp.pl"

        prefix = getattr(self, "prefix", None)
        if prefix is None:
            raise AttributeError("No CSS classes prefix found ",
                    "add prefix to your command like: prefix=<value e.g. i>")
        else:
            self.set_css_classes(prefix)

        yield scrapy.Request(url, self.parse_articles_listing)

    def set_css_classes(self, class_prefix):
        """
        WP webpage periodically rotates preefix to CSS classes. This function
        sets it according to the input value

        Args:
            prefix (str): Value of CSS classes prefix.
        """

        self.article_class = f"{class_prefix}2PrHTUx"
        self.next_page_class = (f"{class_prefix}1xRndDA " +
                                f"{class_prefix}1ZgYxIQ " +
                                f"{class_prefix}2zbd-HY")
        self.article_lead_class = f"article--lead {class_prefix}1HGmjUl"
        self.article_text_class = (f"article--text {class_prefix}FQN8OU2 " +
                                   f"{class_prefix}YwaUr3X")
        self.author_class = (f"signature--author {class_prefix}2aU53vl " + 
                              "desktop")
        self.date_class = (f"signature--when {class_prefix}2VIX-Kh " +
                            "desktop")


    def parse_articles_listing(self, response):

        article_list = response.xpath(f'//a[@class="{self.article_class}"]')
        self.log(f"Found articles: {len(article_list)}")

        for article in article_list:

            link = article.attrib["href"]
            article_url = response.urljoin(link)
            yield scrapy.Request(article_url,
                                 callback=self._parse_article_page,
                                 cb_kwargs={'url': article_url})

        # Need to itarate over generator's results
        next_pages = self._next_page(response)
        for next_page in next_pages:
            yield next_page

    def _parse_article_page(self, response, url):

        lead = self.extract_div_text(response, self.article_lead_class, "div", "p")
        article_text = self.extract_div_text(response, self.article_text_class, "div", "p")
        author_raw = self.extract_div_text(response, self.author_class, "span")
        date_raw = self.extract_div_text(response, self.date_class, "div", "span")
        
        # Getting rid of a prefix to author name that sometimes exists
        author = author_raw.lstrip("oprac.")

        # Getting rid of "Today" etc. prefix
        date = ' '.join(date_raw.split(' ')[-2:])

        yield {
            'date': date,
            'author': author,
            'lead': lead,
            'text': article_text,
            'url': url
        }


    def extract_div_text(self, response, css_class, xpath_first_node,
                         xpath_second_node=None):
        """
        This function extract text from a list of 

        Args:
            response (HtmlResponse): Response of HTML GET method from which
                                     you want to extract text from.
            css_class (str): CSS selector of divs you want to extract text 
                             from.  
            css_class (str): CSS selector of divs you want to extract text 
                             from.  
            css_class (str): CSS selector of divs you want to extract text 
                             from.  

        Returns:
            full_text (str): Text from all divs joine into one string.
        """
        if xpath_second_node is None:
            xpath_second_node = ""
        else:
            xpath_second_node = "/" + xpath_second_node
        response_elems = response.xpath(f'//{xpath_first_node}[@class="{css_class}"]{xpath_second_node}')
        
        texts = []
        for elem in response_elems:
            elem_text = elem.xpath("string()").extract()[0]
            texts.append(elem_text)
        
        full_text = ' '.join(texts)

        return full_text

    def _next_page(self, response):
        """
        This function calls the next page and calls parse() to process it.

        Args:
            response (HtmlResponse): Response of HTML GET method on which 
                                     you want to find next_page button

        Yields:
            request: 
        """
            
        next_page_selector = response.xpath(f'//a[@class="{self.next_page_class}"]')

        for next_page in next_page_selector:
            next_page = next_page.attrib["href"]

            if next_page is not None:
                page_num = int(next_page.strip('/'))
                next_page = response.urljoin(next_page)

                if page_num < 1:
                    yield scrapy.Request(next_page, callback=self.parse)

        
