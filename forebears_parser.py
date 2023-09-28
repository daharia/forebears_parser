from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

DRIVER_PATH = '../chromedriver.exe'
URL_BEFORE = 'https://forebears.io/'
URL_AFTER_SURNAME = '/surnames'
URL_AFTER_FORENAME = '/forenames'

black_list = ['None', 'Names', 'Places', 'Login', 'Forgot password?', 'About', 'Contact', 
              'Copyright',  'Privacy', 'Credits', 'API', 'Do Not Sell My Personal Information',
              'Change Consent', 'Forenames', 'Surnames', 'Genealogical Resources', 'England & Wales Guide']

countries = [ 'united-states', 'england', 'germany', 'france', 'spain', 'portugal' ]  # If you need, add a new country 

def get_page(driver, url):
    try:
        driver.get(url)
    except Exception as err:
        print(err)
        return 0
    return driver.page_source

def write_to_file(list_names, name_file):
    if len(list_names) == 0:
        return
    print(f'Writing a list of {len(list_names)} lengh in file {name_file}.')

    with open('result/' + name_file, 'w') as f:
        f.write('\n'.join(list_names))

def get_surname(driver, country):
    list_names = []
    page_source = get_page(driver, URL_BEFORE + country + URL_AFTER_SURNAME)
    if page_source == 0:
        return
    
    bs = BeautifulSoup(page_source, 'html.parser')
    params = bs.find_all('a')

    for param in params:
        name = str(param.string)
        if name in black_list:
            continue
        list_names.append(name)
    
    name_file = country + '_surname.txt'

    write_to_file(list_names, name_file)

    driver.delete_all_cookies()

def get_forenames(driver, country):
    list_famele_names, list_male_names = [], []
    page_source = get_page(driver, URL_BEFORE + url + URL_AFTER_FORENAME)
    if page_source == 0:
        return
    
    bs = BeautifulSoup(page_source, 'html.parser')
    params = bs.find_all('tr')

    for param in params:
        name = param.find('a')
        if name == None:
            continue
        famele = param.find('div', attrs={'class':'f'})
        # male = param.find('div', attrs={'class':'m full'})

        if famele is None:
            list_male_names.append(name.string)
        else:
            list_famele_names.append(name.string)

    file_male_name = country + '_forenames_male.txt'
    file_famele_name = country + '_forenames_famele.txt'
    
    write_to_file(list_male_names, file_male_name)

    write_to_file(list_famele_names, file_famele_name)

    driver.delete_all_cookies()

def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(DRIVER_PATH, options=options) # options=options
    
    for country in countries:
        get_surname(driver, country)
        get_forenames(driver, country)
    
    driver.quit()

if __name__ == '__main__':
    main()