import fitz
import spacy
import pandas as pd
import re

def load_pdf_text(pdf_path, start_page, end_page):
    doc = fitz.open(pdf_path)
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("sentencizer")
    
    txt, pg_num, char_ct, token_count, sents, sent_len = [], [], [], [], [], []
    
    for i in range(start_page, end_page + 1):
        pgt = doc.load_page(i).get_text("text").replace('\n', ' ')
        txt.append(pgt)
        sentss = nlp(pgt)
        temp_sents = [s for s in sentss.sents]
        sents.append(temp_sents)
        sent_len.append(len(temp_sents))
        pg_num.append(i)
        token_count.append(len(doc.load_page(i).get_text("text")) // 4)
        char_ct.append(len(pgt))
    
    return pd.DataFrame({'page number': pg_num, 'text': txt, 'sentences': sents, 'sentence lengths': sent_len, 'token count': token_count})

def split_list(input_list, slice_size):
    return [input_list[i:i+slice_size] for i in range(0, len(input_list), slice_size)]

def chunk_sentences(text_df, num_sentence_chunk_size=10):
    chnks, num_chnks = [], []
    for item in text_df['sentences']:
        chnks.append(split_list(item, num_sentence_chunk_size))
        num_chnks.append(len(item))
    text_df['sentence_chunks'] = chnks
    text_df["num_chunks"] = num_chnks
    return text_df

def create_chunks_dataframe(text_df):
    pages_and_chunks = []
    for id, item in text_df.iterrows():
        for sentence_chunk in item["sentence_chunks"]:
            chunk_dict = {}
            chunk_dict["page_number"] = item["page number"]
            joined_sentence_chunk = " ".join([str(s) for s in sentence_chunk]).replace("  ", " ").strip()
            joined_sentence_chunk = re.sub(r'\.([A-Z])', r'. \1', joined_sentence_chunk)
            chunk_dict["sentence_chunk"] = joined_sentence_chunk
            chunk_dict["chunk_char_count"] = len(joined_sentence_chunk)
            chunk_dict["chunk_word_count"] = len(joined_sentence_chunk.split(" "))
            chunk_dict["chunk_token_count"] = len(joined_sentence_chunk) // 4
            pages_and_chunks.append(chunk_dict)
    return pd.DataFrame(pages_and_chunks)
