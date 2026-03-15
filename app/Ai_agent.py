
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from openai import OpenAI
import os
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings



client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = SimpleDirectoryReader("app/audio_files").load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = index.as_retriever(similarity_top_k=5)





def retrieve_context(question):
    print("API KEY:", os.getenv("GROQ_API_KEY"))
    nodes = retriever.retrieve(question)
    context = ""
    for node in nodes:
        context += node.text + "\n"

    return context


def ask_groq(question, context):

    prompt = f"""
    Analiza la siguiente transcripción de llamada.
    CONTEXTO:
    {context}
    PREGUNTA:
    {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Eres un asistente que analiza llamadas telefónicas. se debe revisar el texto a profundudidad. puede que lo que se te pase venga de dos o más llamadas debe de contemplarse todos los temas. mantente dentro del tema y si no has la advertencia"},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content