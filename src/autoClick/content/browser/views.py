# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import requests
from bs4 import BeautifulSoup
from random import randint

class AutoClickView(BrowserView):
    template = ViewPageTemplateFile("templates/autoclick_view.pt")
    def __call__(self):
        portal = api.portal.get()
        url = api.content.find(portal['web-site-url'])[0].Description
        self.autoClick(url)
        return self.template()

    def autoClick(self, web_site_url):
        url = web_site_url
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            count = 0
            while count < 3 :
                hrefList = []
                try:
                    hrefList= driver.find_elements_by_partial_link_text('')
                    if len(hrefList) == 0:
                        driver.back()
                        hrefList= driver.find_elements_by_partial_link_text('')
                    elem = hrefList[ randint(0,len(hrefList)-1) ]
                    if elem.is_displayed() and self.isImage(elem.get_attribute('href')) and url in elem.get_attribute('href') or '/' == elem.get_attribute('href')[0]:
                        href = elem.get_attribute('href') 
                        wait = WebDriverWait(driver, 3)
                        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, elem.text)) )
                        elem.click()
                        count += 1
                        print '{}, {} '.format(count, href)
                except TimeoutException as ex:
                    print 'TimeoutException'
                    continue
                except Exception as ex:
                    print 'Exception: {}'.format(ex)
                    print ex
                    continue
        except Exception as ex:
            print 'Error: {}'.format(ex)
        driver.quit()
        print 'ok~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

    def isImage(self, url):
        imgList = ['.gif', '.jpg', '.jpeg', '.png']
        for imgType in imgList:
            if imgType in url:
                return False

        return True
