import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WalmartSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ['walmart.com']
    start_urls = ['https://www.walmart.com/search/?query=shoes']

    def __init__(self, *args, **kwargs):
        super(WalmartSpider, self).__init__(*args, **kwargs)
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)

    def parse(self, response):
        self.driver.get(response.url)

        # Wait until the products are loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-item-id]'))
        )

        # Extract product elements
        products = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-item-id]')

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, 'span[data-automation-id="product-title"]').text
            except:
                title = 'N/A'
            try:
                price = product.find_element(By.CSS_SELECTOR, 'div[data-automation-id="product-price"]').text
            except:
                price = 'N/A'
            try:
                product_link = product.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except:
                product_link = 'N/A'
            try:
                image_link = product.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            except:
                image_link = 'N/A'    
            yield {
                'title': title,
                'price': price,
                'product_link' : product_link,
                'image_link': image_link,
            }

        self.driver.quit()

    def closed(self, reason):
        self.driver.quit()

