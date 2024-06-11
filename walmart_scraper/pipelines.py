import gspread
from oauth2client.service_account import ServiceAccountCredentials
from scrapy.exceptions import DropItem

class GoogleSheetsPipeline:
    def __init__(self, credentials_file):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open('mengstuyaregal').sheet1  # Replace with your Google Sheet name

        # Clear the existing content in the sheet
        self.sheet.clear()

        # Write the headers
        self.sheet.append_row(['Title', 'Price', 'Product Link', 'Image Link'])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            credentials_file=crawler.settings.get('GOOGLE_SHEETS_CREDENTIALS_FILE')
        )

    def process_item(self, item, spider):
        # Write the item to Google Sheets
        try:
            self.sheet.append_row([item['title'], item['price'], item['product_link'], item['image_link']])
        except Exception as e:
            raise DropItem(f"Failed to write item to Google Sheets: {e}")

        return item
