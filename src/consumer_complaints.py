"""
Author: Navita Jain
Verison: Python3

Problem: Given consumer complaint data against companies regarding different financial products.
Identify the number of complaints filed and how they're spread across different companies.

Input:
[Date received,Product,Sub-product,Issue,Sub-issue,Consumer complaint narrative,Company public response,Company,State,ZIP code,Tags,Consumer consent provided?,Submitted via,Date sent to company,Company response to consumer,Timely response?,Consumer disputed?,Complaint ID]
[2019-09-24,Debt collection,I do not know,Attempts to collect debt not owed,Debt is not yours,"transworld systems inc. is trying to collect a debt that is not mine, not owed and is inaccurate.",,TRANSWORLD SYSTEMS INC,FL,335XX,,Consent provided,Web,2019-09-24,Closed with explanation,Yes,N/A,3384392]

Output:
Each line in the output file should list the following fields in the following order:
[product(lowercase),year(from Date received), total number of complaints received for that product and year, total number of companies receiving at least one complaint for that product and year
,highest percentage (rounded) of total complaints filed against one company for that product and year]
["credit reporting, credit repair services, or other personal consumer reports",2019,3,2,67]
[debt collection,2019,1,1,100]


"""

# import libraries
import sys
import csv
from datetime import datetime
import warnings
from collections import Counter


class Product(object):
    """ A class Product and it's data structure store list of companies receiving complaints for a product, year pair"""

    def __init__(self):
        # dict of {tuple(str,str): list of str} = {(product,year): [companies receive complains]}
        self.complain_dict = {}
        # list of sorted tuple(str,str) = [sorted (product,year)]
        self.sort_key = []

    def add_company(self, key_pair, company_name):   #create test
        """
        add key(product,year) and the value company to complain_dict attribute
        :param key_pair: tuple of (str, str) = (product,year)
        :param company_name: str
        :return: None
        """
        if key_pair in self.complain_dict:
            self.complain_dict[key_pair].append(company_name)
        else:
            self.complain_dict[key_pair] = [company_name]

    def sort_dict(self): #create test if prod and year are sorted
        """
        sort and store complain_dict's key(product,year), s.t. product's alphabetically and year's ascending
        :return: None
        """
        self.sort_key = sorted(self.complain_dict.keys())

    def generate_stats(self):
        """
        calculate stats on Product attribute complain_dict and sort_key
        :return output_list: list of list of [str, str, str, str, str] =
                                 list of [product, year, total_complains, unique_companies, %age of most complains against a company]
        """
        output_list = []

        # k-> sorted(product,year)
        for k in self.sort_key:

            # get value from dictionary for key k
            company_complaints = self.complain_dict[k]

            # Counter returns a dictionary of company as key and occurrence/# of complaints as value
            count_company = Counter(company_complaints)

            # total complaints for a company
            total_complaints = sum(count_company.values())

            # number of companies receiving at least one complaint for key(product,year)
            unique_companies = len(count_company.keys())

            # rounded highest percentage of most complaints against a company for that key(product,year)
            highest_percent = round((max(count_company.values()) / total_complaints) * 100)

            # list of list of [product, year, total_complains, unique_companies, highest_percent]
            output_list.append([k[0], k[1], str(total_complaints), str(unique_companies), str(highest_percent)])

        return output_list


def read_complaint_data():
    """
    a generator function to read input file, memory efficient
    :return: generator object for each row of input file
    """
    with open(COMPLAIN_INPUT_FILE, mode='r') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row


def parse_output(output_list):
    """
    from list of output produce a concatenated string that can be written to output file and
                        parse the product name for comma(,) and enclose it into a quotes
    :param output_list: list of list of [str, str, int, int, int] =
                        list of [product, year, total_complains, unique_companies, highest_percent]
    :return: string of comma separated values
                        str(product, year, total_complains, unique_companies, highest_percent]
    """

    # if product name has comma enclose it in quotes
    if len(output_list[0].split(',')) > 1:
        output_list[0] = '"' + output_list[0] + '"'

    # string of comma separated values
    return ",".join(output_list)


def check_bad_records(row):
    """
    check for missing records or bad records in columns Date received, Company, Product
    :param row: row of input file
    :return: None
    """
    try:
        datetime.strptime(row['Date received'], "%Y-%m-%d")
    except ValueError as e:
        print('skipping row because Date received', e)
        return True
    finally:
        if row['Product'] == "" or row['Company'] == "":
            warnings.warn('Skipping row because found missing values in either/both Product and Company column')
            return True
    return False


def write_output(output_list):
    """
    function to creates and write output file
    :param output_list: list of list of [str, str, str, str, str] =
                        list of [product, year, total_complains, unique_companies, highest_percent]
    :return: None
    """
    # generates required output string format to be written to file
    final_output = list(map(parse_output, output_list))
    try:
        # write to output file
        output_file = open(COMPLAIN_OUTPUT_FILE, "w")
        output_file.write("\n".join(final_output))
        output_file.close()
    except Exception as e:
        print('Problem with Input file and folder', e)


if __name__ == '__main__':

    # input file path
    try:
        COMPLAIN_INPUT_FILE = sys.argv[1]
    except Exception as e:
        print('Problem with Input file and folder', e)

    # output file to output directory
    COMPLAIN_OUTPUT_FILE = sys.argv[2]

    print("Working to create output file....")

    # instantiate Product class
    a = Product()

    # yield data
    for row in read_complaint_data():

        # check of bad/missing record
        if check_bad_records(row):
            continue

        # convert date to year
        year = '{:%Y}'.format(datetime.strptime(row['Date received'], "%Y-%m-%d"))
        product = row['Product'].lower()
        company = row['Company']
        # unique product year pair
        key = (product, year)

        # add company to the Product attribute company_complain
        a.add_company(key, company)

    # sort and ordered dict of Product attribute company_complain
    a.sort_dict()

    # generate stats
    output_list = a.generate_stats()

    # write to output file
    write_output(output_list)

    print("Program completed successfully. Output written to file %s" % COMPLAIN_OUTPUT_FILE)





