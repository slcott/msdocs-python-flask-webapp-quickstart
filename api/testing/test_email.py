

# from api.emails import get_emails

import sys

sys.path.append('..')
from email_database import EmailDatabase



def test_get_emails():
    assert len(EmailDatabase.fetch_email_contents()) > 0
    
    
if __name__ == "__main__":
    emails = EmailDatabase.fetch_email_contents()
    print(emails)
    