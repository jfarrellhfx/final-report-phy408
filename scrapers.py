"""
Jack Farrell, University of Toronto, April 2021

Functions to pull data from web pages on comichron and box office mojo, given
the URL of the page
"""
# imports
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt


def read_comichron(URL):
    """
    Get data from comichron, an internet database for comic book information

    :param URL: URL of the web page we want to pull data from
    :return: a string that is to be saved to a csv.  Columns are title,
    publisher, price, and earnings
    """

    # get the web page
    html = requests.get(URL)

    # use beautifulsoup to turn the web page into a nice file structure
    soup = BeautifulSoup(html.text, features="html.parser")

    # initalize an empty string to hold the contents we will return
    file_content = ""

    # the first row of the csv file we will eventually save (initalizing
    # variables to hold all the data we get_
    title = "title"
    units = "units"
    price = "price"
    publisher = "publisher"

    # annoyingly, comichron changed their format in December 2017, adding
    # another column.  So we need to tell the program which column to look
    # for which data
    if float(URL[45:49]) > 2017 or "2017-12" in URL:
        publisher_index = 6
        units_index = 7
    else:
        publisher_index = 5
        units_index = 6

    # find a table in the html we are studying
    table = soup.find('table', attrs={'id': 'Top300Comics'})

    # go through every row of the table
    for row in table.findAll("tr"):

        # go through each cell in the row and save the corresponding data
        i = 0
        for td in row.findAll("td"):

            # title
            if i == 2:
                title = td.text
                title = ''.join([c for c in str(title) if ord(c) < 128])

            # publisher
            if i == publisher_index:
                publisher = td.text

            # price
            if i == 4:
                price = td.text
                price = price.replace("$", "")
                if price == "n.a.":
                    price = "4.99"
                price = float(price)

            # number of units sold
            if i == units_index:
                units = td.text
                units = units.replace(",", "")
                units = float(units)

            i = i + 1

        # assemble into a line to save to our csv
        line = "{},{},{},{}\n".format(title, price, publisher, units)

        # add to the content string
        file_content = file_content + line

    # return the content string
    return file_content


def read_box_office_mojo(URL):
    """

    Get data from comichron, an internet database for comic book information

    :param URL: URL of the web page we want to pull data from
    :return: a string that is to be saved to a csv.  files are date
    and earnings
    """
    # read html at URL
    html = requests.get(URL)

    # use BeatifulSoup to convert to a nice file structure
    soup = BeautifulSoup(html.text, features="html.parser")

    # find the table in the web page
    table = soup.find('table')

    # initalize the first line of our file
    date = "date"
    earnings = "earnings"

    # initalize file content as empty string
    file_content = ""

    # go through every row in the table
    for row in table.findAll('tr'):

        # go through every cell in the table row and get the data we wany
        i = 0
        for td in row.findAll('td'):

            # date
            if i == 0:
                date = td.text

                # get rid of commas, screw up csv
                date = date.replace(",", "")

            # earnings
            if i == 3:
                earnings = td.text

                # get rid of commas, they will screw up the csv.  also
                # get rid of the dollar sign
                earnings = earnings.replace(",", "").replace("$", "")
            i = i + 1

        # assemble a line of the eventual csv
        line = "{},{}\n".format(date, earnings)

        # put the new line into our file string
        file_content = file_content + line

    # return the file string
    return file_content