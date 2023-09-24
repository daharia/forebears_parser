from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

black_list = ['None', 'Names', 'Places', 'Login', 'Forgot password?', 'About', 'Contact', 
              'Copyright',  'Privacy', 'Credits', 'API', 'Do Not Sell My Personal Information',
              'Change Consent', 'Forenames', 'Surnames', 'Genealogical Resources', 'England & Wales Guide']

surname = {'germany': 'https://forebears.io/germany/surnames',
            'france': 'https://forebears.io/france/surnames',
            'spain': 'https://forebears.io/spain/surnames',
            'portugal': 'https://forebears.io/portugal/surnames'}

forenames = {'germany': 'https://forebears.io/germany/forenames',
            'france': 'https://forebears.io/france/forenames',
            'spain': 'https://forebears.io/spain/forenames',
            'portugal': 'https://forebears.io/portugal/forenames'}

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

    with open(name_file, 'w') as f:
        f.write('\n'.join(list_names))

def get_surname(driver, name_file, url):
    list_names = []
    page_source = get_page(driver, url)
    
    bs = BeautifulSoup(page_source, 'html.parser')
    params = bs.find_all('a')

    for param in params:
        name = str(param.string)
        if name in black_list:
            continue
        list_names.append(name)
    
    name_file = name_file + '_surname.txt'

    write_to_file(list_names, name_file)

    driver.delete_all_cookies()

def get_forenames(driver, name_file, url):
    list_famele_names, list_male_names = [], []
    page_source = get_page(driver, url)

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

    file_male_name = name_file + '_forenames_male.txt'
    file_famele_name = name_file + '_forenames_famele.txt'
    
    write_to_file(list_male_names, file_male_name)

    write_to_file(list_famele_names, file_famele_name)

    driver.delete_all_cookies()

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options) # options=options
    
    for key, val in surname.items():
        get_surname(driver, key, val)

    for key, val in forenames.items():
        get_forenames(driver, key, val)


    driver.quit()