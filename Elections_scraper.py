import bs4
import requests
import pandas
import sys
import csv

def input_with_check(user_url: str, user_csv: str) -> tuple:

    constant_url_part = 'https://volby.cz/pls/ps2017nss/'

    if 'https://' not in user_url and 'http://' not in user_url :
        print('Your first argument is not a string of web url')
        print('Program was quit. Check your first argument and try again!')
        quit()
    elif constant_url_part not in user_url:
        print('Your first argument is not a web url for parliament elections in 2017')
        print('Program was quit. Check your first argument and try again!')
        quit()
    elif '.csv' not in user_csv:
        print('Your second argument is not in format "*.csv"')
        print('Program was quit. Check your second argument and try again!')
        quit()
    else:
        try:
            open(user_csv, 'w')
        except FileNotFoundError:
            print('You have probably used the restricted literals in the name of your .csv file')
            print('Program was quit. Check your second argument and again!')
            quit()

    return user_url, user_csv


def correct_shitty_number(numb: str) -> int:
    '''Input is a whole number, given as string
Removes the numbers, including string  "\xa0" instead of empty space for thousands
Numbers in this format are present in the table which is obtained by method pandas.read_html()'''
    return int("".join(numb.split("\xa0")))


class Scraper:
    '''Class for creating objects containing data from a single target webpage (page with table of results)
Thus, the created object represents scraping of complete data, but from a single page.
It does not contain a collection of webpages that are to be scraped'''

    def __init__(self, single_url):

        self.single_url = single_url
        self.table = pandas.read_html(single_url)

    def h3_dict(self) -> dict:
        '''Returns all contents of h3 tags - these build the upper table with basic information on the web
        Output is given as a dict, to support the simplicity of the function usage'''

        def municipality_code() -> str:
            '''Returns a municipility code from URL, when the municipality is requested'''

            str_to_use = self.single_url.partition('obec=')[2]
            iterator = 0
            result = ''

            while True:
                if str_to_use[iterator].isdigit():
                    result += str_to_use[iterator]
                    iterator += 1
                else:
                    break

            return result

        request = requests.get(self.single_url)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        h3_tags = soup.find_all('h3')
        h3_texts = [tag.contents[0].strip('\n') for tag in h3_tags if 'Výsledky' not in tag.contents[0]]

        result = {}
        for text in h3_texts:
            result[text.partition(': ')[0]] = text.partition(': ')[2]
            if text.partition(': ')[0] == 'Obec':
                result['Kód obce'] = municipality_code()

        return result

    def results_of_parties(self) -> dict:
        '''Returns results (votes) for all candidating parties in the given district'''

        def list_of_parties() -> list:
            '''Generates list of parties that were voted in the district
        It is generated from the pandas.read_html() table from the column 0
        The reason is that the names of parties in column 1 are destroyed due to problems with diacritics'''

        # Tato ohavná proměnná je ostuda, ale nenapadlo mě lepší řešení
        # Na vytažení volebních dat používám pandas.read_html(), která má problémy s diakritikou :-(
        # Názvy stran byly tak zkomolené, že by je jedinec bez znalosti politické historie nerozluštil

            registr = ['',
                       'Občanská demokratická strana',
                       'Řád národa - Vlastenecká unie',
                       'CESTA ODPOVĚDNÉ SPOLEČNOSTI',
                       'Česká strana sociálně demokratická',
                       'Volte Pravý Blok',
                       'Radostné Česko',
                       'STAROSTOVÉ A NEZÁVISLÍ',
                       'Komunistická strana Čech a Moravy',
                       'Strana zelených',
                       'ROZUMNÍ - stop migraci a diktátu EU',
                       'Společnost proti developerské výstavbě v Prokopském údolí',
                       'Strana svobodných občanů',
                       'Blok proti islamizaci - Obrana domova',
                       'Občanská demokratická aliance',
                       'Česká pirátská strana',
                       'OBČANÉ 2011-SPRAVEDLNOST PRO LIDI',
                       'Unie H.A.V.E.L.',
                       'Česká národní fronta',
                       'Referendum o EU	Referendum o Evropské unii',
                       'TOP 09',
                       'ANO 2011',
                       'Dobrá volba 2016',
                       'Sdružení pro republiku',
                       'Křesťanská a demokratická unie',
                       'Česká strana národně sociální',
                       'REALISTÉ',
                       'SPORTOVCI',
                       'Dělnická strana sociální spravedlnosti',
                       'Svoboda a přímá demokracie',
                       'Strana Práv Občanů',
                       'Národ Sobě'
                       ]

            return registr

        def column_to_list(column: int) -> list:
            output_lst = []

            for i in range(1, len(self.table)):
                for j in self.table[i].iloc[:, column].tolist():
                    try:
                        output_lst.append(int(j))
                    except ValueError:
                        try:
                            output_lst.append(correct_shitty_number(j))
                            continue
                        except ValueError:
                            break

            return output_lst

        all_parties = list_of_parties()
        results = dict(zip(column_to_list(0), column_to_list(2)))

        output_dict = {}
        for i in range(1, len(all_parties)):
            if i not in results.keys():
                output_dict[all_parties[i]] = 0
            else:
                output_dict[all_parties[i]] = results[i]

        return output_dict

    def votes(self) -> dict:
        '''Returns tuple of delivered votes and valid votes in the given municipality'''

        legend = ['Vydané obálky', 'Odevzdané obálky', 'Platné hlasy']
        result = [self.table[0].iat[0, -6], self.table[0].iat[0, -3], self.table[0].iat[0, -2]]
        output_dict = dict(zip(legend, result))
        for key in output_dict.keys():
            try:
                output_dict[key] = int(output_dict[key])
            except ValueError:
                output_dict[key] = correct_shitty_number(output_dict[key])

        return output_dict


class Driver:
    '''This class works with the input parameter input_url
From the webpage having input_url, all hyperlinks are used to access the referenced webpages that are to be scraped
Collection of all these scrapings is created as a sequence of objects of class Scraper
This class also disposes with method for exporting data from whole collection to the .csv file'''

    def __init__(self, input_url):

        def target_links() -> list:
            '''Returns list of URLs for every municipality in the district, chosen by the user'''

            constant_url_part = 'https://volby.cz/pls/ps2017nss/'
            if 'ps311' not in input_url:
                if input_url == 'https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ':
                    links = [f'https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={i}' for i in range(1, 15)]
                else:
                    a_tags = bs4.BeautifulSoup(requests.get(input_url).text, 'html.parser').body('a')
                    links = [constant_url_part + link.get('href') for link in a_tags if 'vyber' in link.get('href')]

                # Removing duplicates
                if len(links) > 1:
                    links = list(set(links))

            else:
                links = [input_url]

            return links

        self.input_url = input_url
        self.collection = [Scraper(link) for link in target_links()]

    def create_csv(self, filename) -> None:

        temp = self.collection[0]
        header = [*temp.h3_dict().keys(), *temp.votes().keys(), *temp.results_of_parties().keys()]

        with open(filename, 'w') as file:
            csv.writer(file).writerow(header)
            for item in self.collection:
                single_row = [*item.h3_dict().values(), *item.votes().values(), *item.results_of_parties().values()]
                csv.writer(file).writerow(single_row)

# Body of the program
user_url, user_csv = input_with_check(sys.argv[1], sys.argv[2])
Driver(user_url).create_csv(user_csv)
print('Dear User, your scraping was finished. Good work with your CSV!')


