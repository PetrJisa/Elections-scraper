import bs4
import requests
import pandas
import sys
import csv

constant_url_part = 'https://volby.cz/pls/ps2017nss/'

def input_with_check(user_url: str, user_csv: str) -> tuple:
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

def target_links(input_url: str) -> list:
    '''Returns list of URLs for every municipality in the district, chosen by the user'''

    if 'ps311' not in input_url:
        a_tags = bs4.BeautifulSoup(requests.get(input_url).text, 'html.parser').body('a')
        links = [constant_url_part + link.get('href') for link in a_tags if 'vyber' in link.get('href')]

        # removing duplicates in links that occur from unknown reason (to me)
        # They are always 'together' so the next for cycle kills them
        if len(links) > 1:
            for i in range(len(links) - 1, 0, -1):
                if links[i] == links[i - 1]:
                    del links[i]
    else:
        links = [input_url]

    return links

def h3_dict(link: str) -> dict:
    '''Returns all contents of h3 tags - these build the upper table with basic information on the web
    Output is given as a dict, to support the simplicity of the function usage'''

    request = requests.get(link)
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    h3_tags = soup.find_all('h3')
    h3_texts = [tag.contents[0].strip('\n') for tag in h3_tags]

    result = {}
    for text in h3_texts:
        result[text.partition(': ')[0]] = text.partition(': ')[2]
        if text.partition(': ')[0] == 'Obec':
            result['Kod obce'] = municipality_code(link)

    return result

# print(bs4.BeautifulSoup(requests.get(target_links(user_url)[0]).text, 'html.parser').body('td'))

def get_table(link: str):
    ''''Creates pandas data frame from data for municipality'''
    return pandas.read_html(link)

def correct_shitty_number(numb) ->int:
    '''Input is a whole number, given as integer or string
Removes the numbers, including string  "\xa0" instead of empty space for thousands
Numbers in this format are present in the table which is obtained by method pandas.read_html()'''
    return(int(str(numb.partition("\xa0")[0]) + str(numb.partition("\xa0")[2])))


def list_of_parties(table) -> list:
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

    output_lst = []

    for i in range(1, len(table)):
        for j in table[i].iloc[:, 0].tolist():
            try:
                output_lst.append(registr[int(j)])
            except ValueError:
                break

    return output_lst

def results_of_parties(table) -> list:
    '''Returns results (votes) for all candidating parties in the given district'''

    output_lst = []

    for i in range(1, len(table)):
        for j in table[i].iloc[:, 2].tolist():
            try:
                output_lst.append(int(j))
            except ValueError:
                try:
                    output_lst.append(correct_shitty_number(j))
                    continue
                except ValueError:
                    break

    return output_lst

def votes(table) -> tuple:
    '''Returns tuple of delivered votes and valid votes in the given municipality'''

    result = [table[0].iat[0, -6], table[0].iat[0, -3], table[0].iat[0, -2]]
    for i in range(len(result)):
       try:
           result[i] = int(result[i])
       except ValueError:
           result[i] = correct_shitty_number(result[i])

    return tuple(result)

def municipality_code(link: str) -> str:
    '''Returns a municipility code from URL, when the municipality is requested'''

    str_to_use = link.partition('obec=')[2]
    iterator = 0
    result = ''

    while True:
        if str_to_use[iterator].isdigit():
            result += str_to_use[iterator]
            iterator += 1
        else:
            break

    return result

def header(link: str) -> list:
    '''Prepares the header for the output .csv file'''

    table = get_table(link)
    return [*h3_dict(link).keys(), 'Vydané obálky', 'Odevzdané obálky', 'Platné hlasy', *list_of_parties(table)]


def row(link: str) -> list:
    '''Prepares a single row of results for the output .csv file'''

    table = get_table(link)
    return [*h3_dict(link).values(), *votes(table), *results_of_parties(table)]


def rows(all_links: list) -> list:
    '''Collects all rows for the output .csv file'''

    result = []
    for link in all_links:
        result.append(row(link))

    return result

def export_results(first_row: list, other_rows: list, filename: str) -> None:
    '''Exports results to csv file'''

    with open(filename, 'w') as file:
        csv.writer(file).writerow(first_row)
        csv.writer(file).writerows(other_rows)

scraping_url, output_file = input_with_check(sys.argv[1], sys.argv[2])
scraping_links = target_links(scraping_url)
csv_header = header(scraping_links[0])
csv_data = rows(scraping_links)
export_results(csv_header, csv_data, output_file)







