import fitz  # PyMuPDF
import openai

# OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = ""
#openai.api_base = "https://api.together.xyz/v1"
#openai.api_key = ""



def extract_text_from_pdf(pdf_path, chunk_size=30000):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    
    # Split text into smaller chunks (within token limit)
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks    



def ask_llm(question, chunks):
    """Use OpenAI's GPT API to answer questions based on extracted text."""
    insights = []
    for idx, chunk in enumerate(chunks):
        prompt = f"""
        Analyze this section of the company's quarterly financial report. Summarize key highlights such as revenue, net profit, EPS, growth, risks, and future outlook.
        
        {chunk}
        """
        client = openai.OpenAI()  # Create a client instance
        response = client.chat.completions.create(
            model="gpt-3.5-turbo" ,
            messages=[
                {"role": "system", "content": "You are an AI that extracts answers from documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3

        )

        chunkresponse = response.choices[0].message.content.strip()
        insights.append(chunkresponse)
        print(f"Processed chunk {idx+1}/{len(chunks)}")
        #print(chunkresponse)
    return generate_final_summary("\n\n".join(insights))


#  Function to ask Together.ai model a question
def ask_together_ai(question, chunks):
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    
    response = openai.ChatCompletion.create(
        #model="mistralai/Mistral-7B-Instruct-v0.1",  # Use "meta-llama/Llama-2-7b-chat-hf" for LLaMA
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=[{"role": "system", "content": "You are an AI assistant answering questions from a PDF."},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    return response["choices"][0]["message"]["content"].strip()

#  Function to summarize all chunk insights into one final output
def generate_final_summary(combined_text):
    """Takes multiple chunk summaries & generates a final report."""
    prompt = f"""
    Given the following summaries of different sections of a company's quarterly financial report, generate a single, well-structured final summary.

    {combined_text}

    Focus on key financial metrics (revenue, profit, EPS), major developments, challenges, and future guidance.
    """
    client = openai.OpenAI()  # Create a client instance

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an AI financial analyst."},
                  {"role": "user", "content": prompt}],
        max_tokens=700
    )
    return response.choices[0].message.content.strip()


def interactive_pdf_agent(pdf_path):
    """Interactive agent to parse PDF and answer user questions."""
    chunks = extract_text_from_pdf(pdf_path)

    print("\nPDF successfully parsed. You can now ask questions.")
    print("Type 'exit' to quit.\n")
    
    while True:
        question = input("Ask a question: ")
        if question.lower() in ["exit", "quit"]:
            print("Exiting agent. Goodbye!")
            break
        answer = ask_llm(question, chunks)
        #answer = ask_together_ai(question, text)
        print(f"Answer: {answer}\n")

# Example Usage
pdf_path = "okta-last-quarter.pdf"  # Replace with your PDF file
interactive_pdf_agent(pdf_path)
