import requests, sys, os, shutil
from bs4 import BeautifulSoup
from zipfile import ZipFile
# user defined scripts
from . import variables

def get_result(data: dict):
    s = requests.Session()
    with s.get(variables.rooturl, headers=variables.headers) as r:
        if r.status_code != 200:
            print('check your internet connection or make sure the entered roll no range is valid')
            sys.exit(0)
        #get the csrf token
        csrf_token = BeautifulSoup(r.text, 'html.parser').find('meta', {'name':'csrf-token'})['content']

    dir_name = "{}-{}-{}-Semester".format(data['dept'],data['year'],variables.folder[data['sem']]) #final name of the zip file
    _dir = os.path.join(os.path.dirname(__file__),dir_name) #path for temporary storage of the files on server

    if not os.path.exists(_dir):
        os.makedirs(_dir)

    variables.data['_token'] = csrf_token
    variables.data['SEMCODE'] = variables.semcode[data['sem']]

    for rollno in range(data['start'], data['end']+1):
        variables.data['ROLLNO'] = str(rollno)
        with s.post(variables.url_pdf, data=variables.data, headers=variables.headers) as r:
            with open("{}\{}.pdf".format(_dir,rollno), 'wb') as f:
                f.write(r.content)

    create_zip(dir_name) # function call for creating the zip

    _dir = os.path.join(os.path.dirname(__file__), dir_name) # get the parent folder of the temporary files
    shutil.rmtree(_dir) #remove the tempory files

    return '{}.zip'.format(dir_name) #return the final zip name

def create_zip(dir_name):
    """creates the zip file
    
    Arguments:
        dir_name {str} -- name of the final zip
    """
    _dir = os.path.join('scripts\{}'.format(dir_name))
    with ZipFile('{}.zip'.format(dir_name), 'w') as f:
        print("hi")
        for foldername, _, filenames in os.walk(_dir):
            print(filenames)
            for filename in filenames:
                print(foldername)
                f.write('scripts\{}\{}'.format(dir_name, filename),os.path.basename('scripts\{}\{}'.format(dir_name, filename)))
