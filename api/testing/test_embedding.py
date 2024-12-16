
import sys

sys.path.append('..')
from keywords import get_keywords
from embeddings_search import get_chunks, search, SONGS, search_chunks, search_indices, search_indices_by_chunk
from email_database import EmailDatabase

    
def test_search():
    results = search("ocean", SONGS, 0, 4)
    assert len(results) == 4
    assert results[0].startswith('Songs of the Sea')
    # print(results)
    
    
def test_search_offset():
    results = search("ocean", SONGS, start=1, top_k=4)
    assert len(results) == 4
    assert results[0].startswith('Mysteries of the deep')
    # print(results)
    
# def test_embedding_search():
#     emails = EmailDatabase.fetch_email_contents()
#     emails_contents_list = [e['contents'] for e in emails if e['contents'] and len(e['contents']) > 0]
#     indices = search_indices("National School Lunch Act", emails_contents_list, top_k=4)
#     # print(emails[0])
#     print(indices)
#     assert indices[0] == 3
    
def test_chunk():
    text = 'a b c. d e f. g h. i'
    assert [x for x in get_chunks(text)] == ['a b c', 'd e f', 'g h']
    
def test_keyword_search():
    email = EmailDatabase.fetch_email(0)
    keywords = get_keywords(email['contents'])
    # print(keywords)
    assert len(keywords) > 0
    assert 'United States Government' in [k[0] for k in keywords]


def test_chunk_embedding_search():
    email = EmailDatabase.fetch_email(0)['contents']
    best_chunks = search_chunks('food', email, top_k=3)
    # for x in zip(*best_chunks):
    #     for xx in x:
    #         print(xx, end='\n\n')
    assert True
    
def test_best_indices():
    emails = EmailDatabase.fetch_email_contents()
    emails_contents_list = [e['contents'] for e in emails if e['contents'] and len(e['contents']) > 0]
    query = 'qualifies as an elementary education'
    results = search_indices_by_chunk(query, emails_contents_list)
    print(results)    
    best_indices = [index for score, index, chunk in results]
    print(best_indices)
    assert best_indices[0] == 1
    
    