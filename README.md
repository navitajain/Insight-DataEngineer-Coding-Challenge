# Insight-DataEngineer-Coding-Challenge
The solution to the [coding challenge](https://github.com/insightdatascience/consumer_complaints) for the Insight Data Engineering Program implemented in Python3.
 
### Task
The challenge is to do the following- 
We are given records of complaints filed by consumers for various financial products in different years. We need to process the input file and generate the below output/stats -
1. Product(lowercase). If Product name has (,)comma in it, enclose the name with double quota("")
2. Year(from Date received)
3. Total number of complaints received for that product and year
4. Unique companies receiving(at least one complaint) for that product and year
5. Highest percentage of total complaints filed against one company for that product and year(round)
Also, sorted by product(alphabetically) and year(ascending)

### Libraries Required
This code uses sys, csv, datetime, collections built-in libraries

### Instructions
The src/consumer_complaints.py can be launched by running run.sh Bash script.

### Inputs
The program takes input/complaints.csv file


### Outputs
The program written result to output.report.csv

### Approach
The code use following approach -
1. The program yields one line of the input file at a time. This avoids reading an entire file into memory and thus avoid out of memory error in case of large files.
2. Filter missing or bad records. The code release warnings when it encounters bad or missing value for columns 'Product', 'Date received', 'Company' and does not process that row.
3. Used dictionary to maintain unique (product,year)->key mapping to companies and a list that stores the sorted tuple(product,year) in expected output format. Finally for every element in sorted list of (product,year) perform Counter operation to generate required stats which are then written to output file.
