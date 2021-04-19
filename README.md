# Elections-scraper

## Goal of the project
This work is a 3rd project in frame of the course _Online Python Academy_, which is provided by _Engeto Academy_. The project is aimed at web scraping. The data for web scraping were chosen to be the results of the Czech Republic parliament elections which took place in October 2017. 

## How to use the script
The Python script is called _Elections_scraper.py_. It is designed to be started from the command line, using 2 input parameters in the fixed order. The first parameter is the URL, from which we want to scrap the data. The second parameter is the name of the .csv file to write the obtained data. 
**For OS Windows, the input command looks like this example: _>python Elections_scraper.py https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101 Elections.csv_**

## More about the input parameters
For the second parameter, which is the _.csv file_, there are no specialties. Only the general rules for the allowed and forbidden characters must be followed. And obviously there must be an appendix .csv in the file name. 
The first parameter is the _url_. There are several possibilities which links are able to be chosen by the user, and the result depends on the choice. Let me declare it is not caused by the wrong coding, but the reason is the structure of the web pages for election results. There are 4 alternatives, which are described below: 

### Input URL is a link to a district
Probably, this will be the best kind of using the script, becase the volume of the scraped data is the highest. Therefore it brings also the highest potential for data analysis.  Examples of such URLs are as follows:
The URL for the district "Benešov": https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
The URL for the district "Praha": https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100
**How can the user be sure he have chosen the URL of this type? It is specific in the last item of the query, which is always in shape _numnuts=WXYZ_**

### Input URL is a link to a municipality, which is divided into municipality districts
This should be a second most interesting choice of the input URL. In this case, the user chose the municipality, but the link leads to a page where there are municipality district to be selected yet. If the script is opened with this kind of input URL, the scraping leads to obtaining the data for all municipality district - one by one, separately. 
Examples of such URLs are as follows: 
The URL for the municipality district selection in frame of "Praha1": https://volby.cz/pls/ps2017nss/ps33?xjazyk=CZ&xkraj=1&xobec=500054
The URL for the municipality district selection in frame of "Cheb" (which is the beautiful city I was born): https://volby.cz/pls/ps2017nss/ps33?xjazyk=CZ&xkraj=5&xobec=554481
**The specifity of this kind of URL is that it has _obec_ in its query, but simultaneously it does not contain _vyber_**

### Input URL is a direct link to overall results for a municipality
Now we are coming to the less interesting choices of the input URL. In this case, the link sends the user to the web page, where there are only the summarized results for the one selected municipality, whether this municipality has municipality districts or it does not. In other words, it returns .csv with only one row. Nevertheless, even this is better than writing down the data from web number by number, I hope.   
Examples: 
The URL for the municipality "Praha1" : https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=1&xobec=500054&xvyber=1100
THe URL for the municipality "Brloh" : https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=545431&xvyber=3102
The specifity of this kind of URL is it simultaneously contins _obec_ and _vyber_ in the query

### Input URL is a direct link to a municipality district
This kind of URL is similar to the previous one - I mean by the effect. It gives only one row to the output .csv file, in this case the row contains data for one municipality district. 
Examples: 
The URL for the municipality district 8 in "Český Krumlov": https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=545392&xokrsek=8&xvyber=3102
**URL of this type is specific in that its query contains _okrsek_**
