import datetime
import urllib
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# �����pURL�B�����p�����[�^������{}
URL_MERCARI = 'https://www.mercari.com/jp/search/?sort_order=price_asc&keyword={}&status_on_sale=1' # �����J��
URL_RAKUMA = 'https://fril.jp/search/{}?order=asc&sort=sell_price&transaction=selling' # ���N�}

# �ň��l�̗v�f�擾�p�Z���N�^
SELECTOR_MERCARI = '.items-box-price' # �����J��
SELECTOR_RAKUMA = '.item-box__item-price' # ���N�}

CAT_CHAR = ' ' # AND�����L�[���[�h�A���p����
NOT_CHAR = '-' # NOT�����L�[���[�h�̖`���ɕt�^���镶���B���N�}�͖��Ή�
DATA_FILE = 'data.csv' # CSV�t�@�C��

# �����L�[���[�h
keywords_all = [
    {
        'and': ['Ibanez', 'TS-9'],
        'not': ['TS9DX', '808', 'TS5']
    },
    {
        'and': ['Ibanez', 'RG350'],
        'not': ['�W�����N']
    },
    {
        'and': ['BOSS', 'GT-1', '�G�t�F�N�^�['],
        'not': ['GT-10', 'GT-100', 'GT-1000', 'GT-1B', 'AC�A�_�v�^', '���ȏ�']
    },
]

def get_min_price(browser, base_url, query_params, selector):
    """�w�肵���L�[���[�h�̏��i�̍ň��l���擾
    :param browser: �u���E�U
    :param base_url: �����pURL
    :param query_params: �A�������L�[���[�h
    :param selector: ���i�̗v�f�̃Z���N�^
    :return: �ň��l�̕�����
    """
    # �擾�������i���̗]�v�ȕ����폜�p����
    dic = str.maketrans({
        '\': '',
        '��': '',
        ',': '',
        ' ': '',
    })

    # �L�[���[�h���G���R�[�h���AURL�ɖ��ߍ���ŃA�N�Z�X
    url = base_url.format(urllib.parse.quote(query_params))

    try:
        # �ň��l�̗v�f���擾���ĕԂ�
        browser.get(url)
        elm_min = browser.find_element_by_css_selector(selector)
    except NoSuchElementException as e:
        print(f'�w�肵���v�f��������܂���ł���:{e.args}')
    except TimeoutException as e:
        print(f'�ǂݍ��݂��^�C���A�E�g���܂���:{e.args}')

    return(elm_min.text.translate(dic)) # �]�v�ȕ������폜���Ă���Ԃ�

# �u���E�U����
browser = webdriver.Chrome('chromedriver.exe')
browser.set_page_load_timeout(30) # �ǂݍ��݃^�C���A�E�g�ݒ�

# CSV�ۑ��p���X�g��p��
record = []

# ���s���̓��t���擾�E�����񉻂��ĕۑ��p���X�g�ɒǉ�
record.append(datetime.date.today().strftime('%Y/%m/%d'))

# ���i���Ƃɍň��l���擾
for keywords in keywords_all:
    # ���i���Ƃ̌����L�[���[�h��A��
    query_params_and = CAT_CHAR.join(keywords['and']) # AND�p
    query_params_not = CAT_CHAR.join([NOT_CHAR + kw for kw in keywords['not']]) # NOT�p

    # �����J���̍ň��l���擾���A�ۑ��p���X�g�ɒǉ��B
    query_params_mercari = query_params_and + CAT_CHAR + query_params_not
    min_price = get_min_price(browser, URL_MERCARI, query_params_mercari, SELECTOR_MERCARI)
    record.append(min_price)

    # ���N�}�̍ň��l���擾���A�ۑ��p���X�g�ɒǉ�
    query_params_rakuma = query_params_and # AND�̂�
    min_price = get_min_price(browser, URL_RAKUMA, query_params_rakuma, SELECTOR_RAKUMA)
    record.append(min_price)

browser.quit() # �u���E�U�I��

# CSV�ɏ�������
try:
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(record)
except OSError as e:
    print(f'�t�@�C�������ŃG���[����:{e.args}')
