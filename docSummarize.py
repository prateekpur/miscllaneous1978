import pypdf
from langchain.chains.summarize import load_summarize_chain
from langchain_community.llms import Ollama
from langchain.docstore.document import Document

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Path to your PDF file
pdf_path = "Allied_Q4AR_December-31-2024.pdf"
pdf_text = extract_text_from_pdf(pdf_path)

# Load the local Ollama Mistral model
llm = Ollama(model="mistral")

# Convert extracted text into LangChain Document format
#docs = [Document(page_content=pdf_text)]
#summarize_chain = load_summarize_chain(llm, chain_type="map_reduce")
#summary = summarize_chain.run(docs)


# Using Refine
docs = [Document(page_content=pdf_text)]
summarize_chain = load_summarize_chain(llm, chain_type="refine")
summary = summarize_chain.run(docs)
print(summary)

#llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

# Using Stuff
#chain = load_summarize_chain(llm, chain_type="stuff")
#result = chain.invoke(docs)
#print(result["output_text"])

# Using Map-Reduce
#chain = load_summarize_chain(llm, chain_type="map_reduce")
#result = chain.invoke(docs)
#print(result["output_text"])

