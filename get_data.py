"""
Jack Farrell, University of Toronto, April 2021

pull monthly comic book figures from comichron from Jan. 2008 to Dec. 2019.
Also pull daily domestic box office gross from every MCU film
"""

# import the two functions defined in scrapers.py
from scrapers import read_comichron, read_box_office_mojo

# pandas
import pandas as pd

# get variables stored in setup.py
from setup import years, months, comics_folder, mcu_folder

years = range(2008, 2020)
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
comics_folder = "data/comics"
mcu_folder = "data/mcu"

# go through every year and month for which we want data.
for year in years:
    for month in months:
        # build the url of our page based on comichron format
        url = 'https://www.comichron.com/monthlycomicssales/{}/{}-{:02}.html'.format(year, year, month)

        # get data
        data = read_comichron(url)

        # save a csv
        with open(comics_folder + "/{}-{:02}.csv".format(year, month), 'w') as f:
            f.write(data)

        # log progress
        print("Finished year {} month {:02}".format(year, month))


# read the mcu_config (assembled by hand!) to figure out the URL of each MCU
# film's data on box office mojo
mcu_config = pd.read_csv("mcu_config.csv")

# go through every mcu film (i.e. rows in our config file)
for i in range(len(mcu_config["name"])):

    # read the "id" of the film from the config file
    id = mcu_config["id"][i]

    # get the data (by assemblng the url of the movie on box office mojo using
    # the id
    data = read_box_office_mojo("https://www.boxofficemojo.com/release/{}/?ref_=bo_rl_tab#tabs".format(id))

    # save a csv
    with open(mcu_folder + "/" + "{}.csv".format(mcu_config["name"][i].replace(" ", "_")).format(year, month), 'w') as f:
        f.write(data)

    # log progress
    print("just did {}".format(mcu_config["name"][i]))