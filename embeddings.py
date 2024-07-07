import torch
import numpy as np
from sentence_transformers import SentenceTransformer, util

def load_model(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    return SentenceTransformer(model_name)

def encode_chunks(pages_and_chunks, model, device='cuda'):
    for item in pages_and_chunks:
        item["embedding"] = model.encode(item["sentence_chunk"], device=device)
    return pages_and_chunks

def save_embeddings_to_file(pages_and_chunks, filepath):
    df = pd.DataFrame(pages_and_chunks)
    df.to_csv(filepath, index=False)

def load_embeddings_from_file(filepath):
    df = pd.read_csv(filepath)
    df["embedding"] = df["embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep=" "))
    return df

def create_tensor_embeddings(df, device='cuda'):
    return torch.tensor(np.stack(df["embedding"].tolist(), axis=0), dtype=torch.float32).to(device)
