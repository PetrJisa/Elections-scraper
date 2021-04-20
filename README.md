# Elections-scraper

## Goal of the project
This work is a 3rd project in frame of the course _Online Python Academy_, which is provided by _Engeto Academy_. The project is aimed at web scraping. The data for web scraping were chosen to be the results of the Czech Republic parliament elections which took place in October 2017. 

## How to use the script
The Python script is called _Elections_scraper.py_. It is designed to be started from the command line, using 2 input parameters in the fixed order. The first parameter is the URL of the webpage, from which we want to scrap the data. The second parameter is the name of the .csv file to write the obtained data. The parameters are separated from the python command and from each other only by the space. 

**For OS Windows, the input command looks like this example (do not forget to type them as string and to use the space for their division): _>python Elections_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101" "Elections.csv"_**

## More about the input parameters...
For the second parameter, which is the _.csv file_, there are no specialties. Only the general rules for the allowed and forbidden characters must be followed. And obviously there must be an appendix .csv in the file name. 

The first parameter is the _URL of the webpage, from which we want to scrap the data_. In fact, there are 2 requirements on this parameter:
**1) The URL must contain the constant part _'https://volby.cz/pls/ps2017nss/'_**
**2) Behind the constant part, there must be a query, which links into the web page with elections results for a given area, like _'ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102'_**

The most certain way is to copy the whole links from the web pages, of sure.

## ...And even more about the first input parameter

There are no limits regarding the choice of the area for the scrapping, using the script. However, due to the structure of the web pages, there are 2 types of the link that can be found (and used). 

### Input URL is a link to an area (district), without any subdistricts
Links of this type refers to the summarized results for the chosen district (area), which can be municipality, group of municipalities (district), or even higher districts. Using this kind of link as an input parameter leads to creation of .csv with only one row, containing information about the chosen district only. One can say it is not such a "big wow". Neverheless, in my opinion it is still better compared to writing the numbers down manually.

**These links can be characterized by presence of string "ps311" at the beginning of the query**

Examples of links, belonging to this type: 

Example 1: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=534421&xvyber=2102
Example 2: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=531057&xokrsek=6&xvyber=2102

### Input URL is a link to an area (district), where the subdistricts are chosen from
Using this kind of URL shows the real strenth of the script, because in this case, all data from the links which are present on the webpage, which is reached from this URL, are scrapped into the output .csv file. Thus, when the user gives input URL to the webpage, where even 30 or more subdistricts are offered to be chosen, the script does the filthy job of opening these all links one by one and processing all data gradually, instead of the human. 

** These links can be characterized by absence of string "ps311" at the beginning of the query**

Examples of links, belonging to this type: 

Example 3: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3202
Example 4: https://volby.cz/pls/ps2017nss/ps33?xjazyk=CZ&xkraj=5&xobec=554481

## Examples
The output examples are presented by the added .csv files in this repository. They are obtained, when the rules for entering the input parameters are followed, and the used URL links correspond with the Examples 1 - 4 from the previous chapter. These output files are called 'ExampleX.csv' where X is the number of the example.

## Requirements
The script uses imported modules of the three sides, that must be installed prior to the script usage. The best way is to build-up a separate project with the script, which is running in the virtual environemnt. In that case, the installed modules are only part of the project, while the other projects "do not see them". 
For the modules installation, it is enough to type following command into the link of the virtual environment: **_>pip install module_** where module is the name of the given module. 

**All modules that are necessary to be installed to run the script, are listed in the attached file _"Requirements.txt"_**

## ACKNOWLEDGMENT
In this place, I would like to thank my teachers from Engeto Academy for their effort to teach me the basics of Python. Please, hold on in your teaching, you are really good!

## ENJOY THE SCRAPING!



