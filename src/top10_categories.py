# -*- coding: utf-8 -*-

# ------------------------------------------ Module Imports & Definitions -------------------------------------------- #

# Standard package(s) import ----------------------------------------------------------------------
import json
from builtins import str, range, len, list

import pandas as pd
import re
import sqlite3 as sl


# --------------------------------------------- Top10 Class Definition ----------------------------------------------- #
class Top10:
    """Find the top 10 categories of all papers for a given year.

    Parameters
    -------------------------------------------------------------------------------------
    database: str
        The path to the database to query on.

    Methods
    -------------------------------------------------------------------------------------
    query_columns():
        Query 'columns' from 'table' given as parameters.
    extract_version_year()
        Extract year from last version string in the list of 'versions'.
    extract_update_year()
        Extract year from column 'update_date'.
    top10_categories()
        Get the top 10 categories for last year (picked from versions dates)
    """
    def __init__(self, database):
        # The database to connect to
        self.db = database
        # The connection to the database given as parameter
        self.con = sl.connect(self.db)
        # The DataFrame holding the data to compute
        self.df_data = pd.DataFrame()
        # The text message to return
        self.display = ""

    def query_columns(self, table='ARXIV', columns=['categories', 'versions']):
        """Query 'columns' from 'table' given as parameters.

        Parameters
        -------------------------------------------------------------------------------------
        table: str
            The name of the table to query from.
        columns: list
            The list of columns to query from the table.
        """
        # build query with 'table'and 'columns'
        query = "SELECT " + ", ".join(columns) + " FROM " + table
        # query columns 'categories' and 'versions'
        try:
            self.df_data = pd.read_sql(query, self.con)
        except Exception:
            print(f"Sorry, we can't find table \'{table}\' in the database \'{self.db}\'.")

    def extract_version_year(self):
        """Extract year from last version string in the list of 'versions'."""
        try:
            # define pattern to extract year from last version date
            pattern = re.compile('\d{4}')
            # convert 'versions' string as lists
            self.df_data.versions = self.df_data.versions.map(lambda x: json.loads(x))
            # extract year from field 'created' for last version (index -1)
            self.df_data['version_year'] = self.df_data.versions.apply(
                lambda x: re.findall(pattern, x[-1]['created'])[0]
            )
        except AttributeError:
            print(f"Sorry, we could not find column 'versions' in the DataFrame.")

    def extract_update_year(self):
        """Extract year from column 'update_date'."""
        try:
            # extract year from 'update_year'
            self.df_data['update_year'] = self.df_data['update_date'].apply(lambda x: x.split('-')[0])
        except AttributeError:
            print(f"Sorry, we could not find column 'update_date' in the dataframe.")

    def top10_categories(self, year=2020):
        """Get the top 10 categories for last year.

        Parameters
        -------------------------------------------------------------------------------------
        year: int
            The year on which to extract the top 10 categories.
        """
        # extract last column with 'year' in its label
        col = ''
        for label in self.df_data.keys():
            if 'year' in label:
                col = label
        # extract df for given year only
        df = self.df_data[self.df_data[col] == str(year)].copy()
        # extract top 10 categories
        top10_cat = list(df['categories'].value_counts()[0:10].index)
        # display list as proper text
        self.display = "TOP 10 CATEGORIES FOR YEAR {}: \n".format(str(year))
        for i in range(len(top10_cat)):
            self.display = self.display + "  #" + str(i + 1) + ": " + top10_cat[i] + "\n"


# --------------------------------------------- Top10 Class main function -------------------------------------------- #
def main():
    # path to database
    db_path = './../data/arxiv.db'
    # instantiate Top10 src
    top10 = Top10(db_path)
    # query appropriate columns on top10 object
    top10.query_columns('ARXIV', ['categories', 'versions'])
    # extract year from versions dates
    top10.extract_version_year()
    # compute top10 categories
    top10.top10_categories(2020)
    # return top 10 categories
    print(top10.display)


if __name__ == "__main__":
    main()
