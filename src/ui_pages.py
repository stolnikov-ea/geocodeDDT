from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GeocoderUI:
    # Forward Search (Поиск по адресу)
    URL_DIRECT = "https://nominatim.openstreetmap.org/ui/search.html"
    LOC_ADVANCED_OPTIONS = (By.ID, "searchAdvancedOptions")
    LOC_LIMIT_INPUT = (By.ID, "option_limit")
    LOC_SEARCH_INPUT = (By.ID, "q")

    # Reverse Search (Поиск по координатам)
    URL_REVERSE = "https://nominatim.openstreetmap.org/ui/reverse.html"
    LOC_LAT_INPUT = (By.ID, "reverse-lat")
    LOC_LON_INPUT = (By.ID, "reverse-lon")
    LOC_SEARCH_SECTION = (By.CLASS_NAME, "search-section")
    LOC_SEARCH_BTN = (By.CLASS_NAME, "btn-primary")

    # Результаты поиска
    LOC_RESULTS_CONTAINER = (By.ID, "searchresults")
    LOC_RESULT_ITEM = (By.XPATH, './/div[@data-position="0"]')
    LOC_DETAILS_BTN = (By.CLASS_NAME, "btn-outline-secondary")
    LOC_DETAILS_TABLE = (By.ID, "locationdetails")
    LOC_CENTER_POINT_CELL = (By.XPATH, ".//tr[contains(., 'Centre Point')]//td[2]")
    LOC_ADDRESS_TABLE = (By.ID, "address")
    LOC_FIRST_ADDR_ROW = (By.XPATH, ".//tbody/tr[1]/td[1]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_url(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.find(locator).click()

    def fill(self, locator, text):
        elem = self.find(locator)
        elem.clear()
        elem.send_keys(str(text))

    def open_details_for_first_result(self):
        container = self.find(self.LOC_RESULTS_CONTAINER)
        item = container.find_element(*self.LOC_RESULT_ITEM)
        item.click()
        btn = item.find_element(*self.LOC_DETAILS_BTN)
        btn.click()

    def get_coordinates(self):
        table = self.find(self.LOC_DETAILS_TABLE)
        cell = table.find_element(*self.LOC_CENTER_POINT_CELL)
        lat_str, lon_str = cell.text.split(",")
        return float(lat_str), float(lon_str)

    def get_address_name(self):
        table = self.find(self.LOC_ADDRESS_TABLE)
        row = table.find_element(*self.LOC_FIRST_ADDR_ROW)
        return row.text

    def forward_search(self, address, limit=1):
        self.open_url(self.URL_DIRECT)
        self.click(self.LOC_ADVANCED_OPTIONS)
        self.fill(self.LOC_LIMIT_INPUT, limit)
        self.fill(self.LOC_SEARCH_INPUT, address)
        self.find(self.LOC_SEARCH_INPUT).send_keys(Keys.RETURN)

    def reverse_search(self, lat, lon):
        self.open_url(self.URL_REVERSE)
        self.fill(self.LOC_LAT_INPUT, lat)
        self.fill(self.LOC_LON_INPUT, lon)
        section = self.find(self.LOC_SEARCH_SECTION)
        btn = section.find_element(*self.LOC_SEARCH_BTN)
        btn.click()