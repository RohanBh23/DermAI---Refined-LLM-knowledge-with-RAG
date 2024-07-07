import pdf_processing
import embeddings
import retrieval

def main():
    pdf1_path = r"C:\Users\Rohan Bhatia\Documents\Summer SEM\RAG Project\978-3-031-08057-9.pdf"
    pdf2_path = r"C:\Users\Rohan Bhatia\Documents\Summer SEM\RAG Project\hair-loss.pdf"
    
    text_df1 = pdf_processing.load_pdf_text(pdf1_path, 32, 500)
    text_df2 = pdf_processing.load_pdf_text(pdf2_path, 15, 225)
    
    text_df1 = pdf_processing.chunk_sentences(text_df1)
    text_df2 = pdf_processing.chunk_sentences(text_df2)
    
    df_chunks1 = pdf_processing.create_chunks_dataframe(text_df1)
    df_chunks2 = pdf_processing.create_chunks_dataframe(text_df2)
    
    pages_and_chunks = pd.concat([df_chunks1, df_chunks2]).to_dict(orient='records')
    
    model = embeddings.load_model()
    pages_and_chunks = embeddings.encode_chunks(pages_and_chunks, model)
    
    embeddings.save_embeddings_to_file(pages_and_chunks, "text_chunks_and_embeddings_df.csv")
    
    df = embeddings.load_embeddings_from_file("text_chunks_and_embeddings_df.csv")
    tensor_embeddings = embeddings.create_tensor_embeddings(df)
    
    query = "use of minoxidil"
    retrieval.print_top_results_and_scores(query, tensor_embeddings, pages_and_chunks, model)

if __name__ == "__main__":
    main()
