import glob
from bs4 import BeautifulSoup

from keywords import get_keywords

class EmailDatabase:
    @staticmethod
    def fetch_email_contents():
        ret = []
        i = -1
        for file_path in glob.iglob('/Users/slcott/Dropbox/workplace/lcg/msdocs-python-flask-webapp-quickstart/api/emails/**/*.htm', recursive=True):
            i += 1
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # lines = []
                # try: 
                #     for line in f:
                #     #     line = f.readline()
                #     #     lines.append(line)
                #         line = f.readline()
                #         lines.append(line)
                # except UnicodeDecodeError as e:
                #     print(e)
                # content = ''.join(lines)
                # soup = BeautifulSoup(content, 'html.parser')
                # all_tags = soup.find_all()
                # for tag in all_tags:
                #     print(tag.get_text())
                # # ret.append({ 'file_path': file_path, 'contents': tag.get_text() })
                soup = BeautifulSoup(f, 'html.parser')
                all_tags = soup.find_all('p')
                contents = []
                for tag in all_tags:
                    content = tag.get_text()
                    contents.append(content)
                contents = ' '.join(contents)
                keywords = get_keywords(contents)
                ret.append({ 'id': i, 'file_path': file_path, 'contents': contents, 'keywords': keywords })
                # ret.append({ 'id': i, 'file_path': file_path, 'contents': contents })
                
                
        return ret
    
    def fetch_email(email_id):
        emails = EmailDatabase.fetch_email_contents()
        for e in emails: 
            if e['id'] == email_id:
                return e
