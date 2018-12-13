import PyPDF2
from functools import wraps


def get_or_empty(the_list, index):
    try:
        return the_list[index]
    except IndexError:
        return ''


def get_or_empty_dec(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        the_index = func(self, *args, **kwargs)
        return get_or_empty(self.a_list, the_index)

    return wrapped


class Penerima(object):

    def __init__(self, a_list):
        self.a_list = a_list

    @property
    @get_or_empty_dec
    def nama(self):
        return 0

    @property
    @get_or_empty_dec
    def no_anggota(self):
        return 1

    @property
    @get_or_empty_dec
    def nip(self):
        return 2

    @property
    @get_or_empty_dec
    def nuptk(self):
        return 3

    @property
    @get_or_empty_dec
    def nama_satuan_pendidikan(self):
        return 4

    @property
    @get_or_empty_dec
    def nomor_rekening(self):
        return 5

    @property
    @get_or_empty_dec
    def an_bank(self):
        if len(self.a_list) == 13:
            return 6
        return 90

    @property
    @get_or_empty_dec
    def nama_bank(self):
        if len(self.a_list) == 13:
            return 11
        return 10

    @property
    @get_or_empty_dec
    def nomor_peserta(self):
        if len(self.a_list) == 13:
            return 12
        return 11


def process_page(the_page):
    the_text = the_page.extractText()
    collections = []

    lines = the_text.splitlines()
    if 'No' not in lines:
        return collections

    start = lines.index('No') + 1

    rest_lines = lines[start:]
    separator = 'no peserta'.upper()
    while separator in rest_lines:
        end = rest_lines.index(separator)
        collections.append(Penerima(rest_lines[:end]))
        rest_lines = rest_lines[end + 1:]
    return collections


with open('0003_T_KOTA SURABAYA.pdf', 'rb') as testpdf:
    reader = PyPDF2.PdfFileReader(testpdf)
    collections = []
    print('Please wait while processing')
    for page in range(reader.getNumPages()):
        the_page = reader.getPage(page)
        results = process_page(the_page)
        collections += results
    print(f'total result: {len(collections)}')

    for index, result in enumerate(collections):
        print(f'{index + 1}. {result.nama}')
        print(f'Nip: {result.nip}')
        print(f'NUPTK: {result.nuptk}')
        print(f'NO PESERTA: {result.nomor_peserta}')
        print(f'NRG: {result.no_anggota}')
        print(f'Satuan Pendidikan: {result.nama_satuan_pendidikan}')
        print('Detail bank')
        print(f'Bank {result.nama_bank} a/n {result.an_bank}\n{result.nomor_rekening}')
        print('-' * 10)



