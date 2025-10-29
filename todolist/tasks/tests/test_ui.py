from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tasks.models import Task
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class UITest(StaticLiveServerTestCase):
    def setUp(self):
        # prepare data
        Task.objects.create(
            content = "temp task",
            status = 'undo'
        )

        # selenium firefox driver setting
        options = Options()
        options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"
        self.driver = webdriver.Firefox(
            service=Service("/snap/bin/geckodriver"),
            options=options
        )
        self.driver.get(self.live_server_url)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_list_task(self):
        # assert
        self.driver.implicitly_wait(3)
        self.assertIn('temp task', self.driver.page_source)
        self.assertIn('undo', self.driver.page_source)

    def test_add_task(self):
        # prepare data
        content = 'add task'
        status = 'undo'

        # add task action
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.CLASS_NAME, "btn-add").click()
        self.driver.find_element(By.NAME, "content").send_keys(content)
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        # assert
        self.assertIn(content, self.driver.page_source)
        self.assertIn(status, self.driver.page_source)

    def test_edit_task(self):
        # prepare data
        new_content = 'edit task'
        new_status = 'done'

        # edit task action
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.CLASS_NAME, "btn-edit").click()
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.NAME, "content").send_keys(new_content)
        status_list = self.driver.find_element(By.TAG_NAME, "select")
        Select(status_list).select_by_value(new_status)
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        # assert 
        self.assertIn(new_content, self.driver.page_source)
        self.assertIn(new_status, self.driver.page_source)

    def test_delete_task(self):
        # delete action
        self.driver.implicitly_wait(3)
        self.driver.find_element(By.CLASS_NAME, "btn-delete").click()
        time.sleep(1)

        # assert
        self.assertNotIn('temp task', self.driver.page_source)
