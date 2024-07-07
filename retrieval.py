import torch
import numpy as np
from sentence_transformers import util
from time import perf_counter as timer

def retrieve_relevant_resources(query, embeddings, model, n_resources_to_return=5, device='cuda'):
    query_embedding = model.encode(query, convert_to_tensor=True, device=device)
    start_time = timer()
    dot_scores = util.dot_score(query_embedding, embeddings)[0]
    end_time = timer()
    print(f"[INFO] Time taken to get scores on {len(embeddings)} embeddings: {end_time-start_time:.5f} seconds.")
    scores, indices = torch.topk(input=dot_scores, k=n_resources_to_return)
    return scores, indices

def print_top_results_and_scores(query, embeddings, pages_and_chunks, model, n_resources_to_return=5, device='cuda'):
    scores, indices = retrieve_relevant_resources(query, embeddings, model, n_resources_to_return, device=device)
    for score, idx in zip(scores, indices):
        print(f"Score: {score:.4f}")
        print("Text:")
        print_wrapped(pages_and_chunks[idx]["sentence_chunk"])
        print(f"Page number: {pages_and_chunks[idx]['page_number']}")
        print("\n")
