from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
from typing import List
import re


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


# example sentences used for testing
SONGS = [
  "Beyond Mars (1 hr 15 min): Join space enthusiasts as they speculate about extraterrestrial life and the mysteries of distant planets.",
  "Jazz under stars (55 min): Experience a captivating night in New Orleans, where jazz melodies echo under the moonlit sky.",
  "Mysteries of the deep (1 hr 30 min): Dive with marine explorers into the uncharted caves of our oceans and uncover their hidden wonders.",
  "Rediscovering lost melodies (48 min): Journey through time to explore the resurgence of vinyl culture and its timeless appeal.",
  "Tales from the tech frontier (1 hr 5 min): Navigate the complex terrain of AI ethics, understanding its implications and challenges.",
  "The soundscape of silence (30 min): Traverse the globe with sonic explorers to find the world's most serene and silent spots.",
  "Decoding dreams (1 hr 22 min): Step into the realm of the subconscious, deciphering the intricate narratives woven by our dreams.",
  "Time capsules (50 min): Revel in the bizarre, endearing, and profound discoveries that unveil the quirks of a century past.",
  "Frozen in time (1 hr 40 min): Embark on an icy expedition, unearthing secrets hidden within the majestic ancient glaciers.",
  "Songs of the Sea (1 hr): Dive deep with marine biologists to understand the intricate whale songs echoing in our vast oceans."
]

# https://huggingface.co/sentence-transformers/all-mpnet-base-v2

def search_indices(query, corpora: List[str], start=0, top_k=1) -> List[int]:
    if start is None:
        start = 0
    if top_k is None:
        top_k = 1
    # if fn is None:
    #     fn = lambda x: x
    top_k = min(top_k, len(corpora) - start)
    # print('top_k', top_k)

    # Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')

    # Tokenize sentences
    encoded_input = tokenizer(corpora, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    # print("Sentence embeddings:")
    # print(sentence_embeddings)
    # print(sentence_embeddings.shape)


    # sentence_test = ["saxophone nightclub"]
    sentence_test = [query]
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    # tokenizer = GPT4Tokenizer.from_pretrained('Xenova/text-embedding-ada-002')
    # model = AutoModel.from_pretrained('Xenova/text-embedding-ada-002')

    # Tokenize sentences
    encoded_input = tokenizer(sentence_test, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    query_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    query_embeddings = F.normalize(query_embeddings, p=1, dim=1)

    # print("query embeddings:")
    # print(sentence_test_embeddings)
    # print(query_embeddings.shape)

    cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
    scores = cos(sentence_embeddings, query_embeddings[0])
    # print(scores)
    # best_i = torch.argmax(scores)
    best_k = torch.topk(scores, top_k+start)
    # print(best_k.indices)
    
    # print(best_i)
    # print(sentences[best_i])
    # return sentences[best_i]
    # print([k for k in best_k.indices[start:]])
    # return [corpus[k] for k in best_k.indices[start:]]
    return best_k.indices[start:].tolist()
    


def search(query, corpus: List[str], start=0, top_k=1) -> List[str]:
    indices = search_indices(query, corpus, start, top_k=top_k)
    return [corpus[k] for k in indices]

################################################################################

from itertools import cycle

def search_indices_by_chunk(query, corpora: List[str], start=0, top_k=10) -> List[str]:
    # indices = search_indices(query, corpus, start, top_k=top_k)
    # return [corpus[k] for k in indices]
    best_overall_scores = []
    for i, corpus in enumerate(corpora):
        best_scores, best_chunks = search_chunks(query, corpus, top_k=1)
        #    best_overall_scores.extend(list(zip(best_scores, i)))
        best_overall_scores.append((best_scores[0], i, best_chunks[0]))
    best_overall_scores.sort(reverse=True)
    # best_k_overall_scores = torch.topk(best_overall_scores, top_k+start)
    
    # best_indices = []
    # for score, index, chunk in best_overall_scores:
    #     best_indices.append(index)
    # return best_indices
    return best_overall_scores

def get_chunks(text):
    lo = 0
    for hi in [ i.start() for i in re.finditer('\\.', text) ]:
        yield text[lo:hi].strip()
        lo = hi + 1

def search_chunks(query, corpus: str, top_k=1):
    # Load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    
    
    chunks = [x for x in get_chunks(corpus) if all(y not in x for y in (':', '@', '>;'))]
 
    # Tokenize sentences
    encoded_input = tokenizer(chunks, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

    # sentence_test = ["saxophone nightclub"]
    sentence_test = [query]
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-mpnet-base-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')

    # Tokenize sentences
    encoded_input = tokenizer(sentence_test, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)

    # Perform pooling
    query_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    query_embeddings = F.normalize(query_embeddings, p=1, dim=1)

    cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
    scores = cos(sentence_embeddings, query_embeddings[0])
    # print(scores)

    best_k = torch.topk(scores, top_k)
    best_indices = best_k.indices.tolist()
    best_chunks = [chunks[i] for i in best_indices]
    best_scores = [scores[i].item() for i in best_indices]
    return best_scores, best_chunks
    