import time
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from embeddings_search import search, search_indices, SONGS, search_indices_by_chunk
from email_database import EmailDatabase

app = Flask(__name__)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/search', methods=['GET'])
def get_fake_search():
    return [ 
            { 'id': 1, 'content': 'one'}, 
            {  'id': 2, 'content': 'two'} 
            ]

@app.route('/song_search', methods=['GET'])
def search_songs():
    query = request.args.get('query')    
    results = search(query, SONGS, top_k=5)
    response = []
    for i, result in enumerate(results):
        response.append({'id': i, 'content': result })
    return response

@app.route('/email_search', methods=['GET'])
def search_emails():
    query = request.args.get('query')
    top_k = request.args.get("k", default=None, type=int)
    emails = EmailDatabase.fetch_email_contents()
    # email.sort(lambda x: x['id'])  # should not be necessary
    
    emails_contents_list = [e['contents'] for e in emails if e['contents'] and len(e['contents']) > 0]
    # results = search(query, emails_contents_list, top_k=top_k)
    
    # indices = search_indices(query, emails_contents_list, top_k=top_k)
    results = search_indices_by_chunk(query, emails_contents_list)
    indices = [index for score, index, chunk in results]
    # indices = set(indices)
    print(indices)
    
    emails_dict = { e['id']: e for e in emails }
    
    response = []
    # for i, result in enumerate(results, 1):
    #     response.append({'id': i, 'content': result })
    # for email in emails:
    #     if email['id'] in indices:
    #         response.append(email)
    for i in indices:
        response.append(emails_dict[i])
    return response


@app.route('/emails', methods=['GET'])
def list_emails():
    response = EmailDatabase.fetch_email_contents()
    return response

@app.route('/emails/<int:email_id>', methods=['GET'])
def get_email(email_id):
    # print(email_id)
    email = EmailDatabase.fetch_email(email_id)
    # print(email)
    if email:
        # return { 'contents': email['contents'] }
        return email
    return { 'contents': 'Not Found' }


if __name__ == '__main__':
    app.run()
