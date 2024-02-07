*** Settings ***
Documentation       Working with search news.

Library             Tasks.py
Library             RPA.Browser.Selenium

Task Teardown       Close All Browsers


*** Tasks ***
Using Tasks with Pure Selenium
    Rpa Challenge    months_range=${months_range}    search_phrase=${search_phrase}