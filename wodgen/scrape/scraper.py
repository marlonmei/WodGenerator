import re
from typing import List
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from config import (
    PARSER,
    SLEEP_TIME_INITIAL,
    SLEEP_TIME_SCROLLING,
    NUMBER_OF_SCROLLING,
    SCROLLER
)
from constants import SPECIAL_CHARACTERS


class WorkoutScraper():
    url: str
    soup: BeautifulSoup

    def __init__(self):
        self.driver = webdriver.Firefox()

    def scroll_page(self, number_of_times: int):
        for _ in range(number_of_times):
            self.driver.execute_script(f"window.scrollTo(0,{SCROLLER})")
            sleep(SLEEP_TIME_SCROLLING)

    def extract_raw_content(self, url: str):
        self.driver.get(url)
        sleep(SLEEP_TIME_INITIAL)
        self.scroll_page(number_of_times=NUMBER_OF_SCROLLING)
        raw_page = self.driver.page_source
        self.soup = BeautifulSoup(raw_page, PARSER)

    def extract_class_content(self, title_class: str, html_tag: str) -> List[str]:
        strings = self.soup.find_all(html_tag, class_=title_class)
        return strings

    @staticmethod
    def simple_strip_of_list(list_of_strings: List[str]) -> List[str]:
        return [ele.get_text(separator='\n').strip() for ele in list_of_strings]

    @staticmethod
    def conditional_strip_of_list(list_of_strings: List[str], html_tag: str) -> List[str]:
        results = []

        for string in list_of_strings:
            tag = string.find(html_tag)
            if tag:
                stripped_string = tag.text.strip()
                results.append(stripped_string)
        return results

    def close_session(self):
        self.driver.close()


class StringProcessor:

    @staticmethod
    def replace_special_characters(list_of_strings: List[str]) -> List[str]:
        results = []
        for key, value in SPECIAL_CHARACTERS.items():
            for string in list_of_strings:
                results.append(string.replace(key, value))
        return results

    @staticmethod
    def remove_special_characters(list_of_strings: List[str]) -> List[str]:
        results = []
        for string in list_of_strings:
            results.append(re.sub('[^A-Za-z0-9 ]+', '', string))
        return results

    @staticmethod
    def insert_whitespace_numerical(list_of_strings: List[str]) -> List[str]:
        results = []
        for input_string in list_of_strings:
            output_string = ''
            prev_char = ''
            for char in input_string:
                first_condition = (char.isalpha() and prev_char.isdigit())
                second_condition = (char.isdigit() and prev_char.isalpha())
                if first_condition or second_condition:
                    output_string += ' '
                output_string += char
                prev_char = char
            results.append(output_string)
        return results

    @staticmethod
    def insert_whitespace_alphabetical(list_of_strings: List[str]) -> List[str]:
        results = []
        for input_string in list_of_strings:
            output_string = ''
            for i, char in enumerate(input_string):
                if i < len(input_string) - 1 and char.islower() and input_string[i + 1].isupper():
                    output_string += char + ' '
                else:
                    output_string += char
            results.append(output_string)
        return results

    def process_extensively(self, list_of_strings: List[str]) -> List[str]:
        list_of_strings = self.replace_special_characters(list_of_strings)
        list_of_strings = self.remove_special_characters(list_of_strings)
        list_of_strings = self.insert_whitespace_alphabetical(list_of_strings)
        list_of_strings = self.insert_whitespace_numerical(list_of_strings)
        return list_of_strings

