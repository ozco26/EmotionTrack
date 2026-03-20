
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

def load_documents():
    documents = SimpleDirectoryReader("app/audio_files").load_data()
    index = VectorStoreIndex.from_documents(documents)
    retriever = index.as_retriever(similarity_top_k=5)
    return retriever

def retrieve_context(question):
    retriever = load_documents()
    nodes = retriever.retrieve(question)
    context = ""
    for node in nodes:
        context += node.text + "\n"

    return context


def ask_groq(question, context):

    prompt = f"""
    INSTRUCCIONES:
    - Analiza cuidadosamente TODO el CONTEXTO proporcionado.
    - El contexto puede contener UNA o VARIAS llamadas mezcladas.
    - NO ignores ninguna parte relevante.
    - NO inventes información que no esté explícitamente en el texto.
    - Si la información es insuficiente o ambigua, indícalo claramente.

    TAREA:
    Responde la PREGUNTA basándote ÚNICAMENTE en el CONTEXTO.

    FORMATO DE RESPUESTA:
    1. Respuesta directa a la pregunta
    2. Evidencia (fragmentos o ideas del texto que respaldan la respuesta)
    3. Observaciones (opcional: inconsistencias, múltiples llamadas, ambigüedad)
    - Si la respuesta no está en el contexto, responde: "No se encuentra información suficiente en la transcripción."

    CONTEXTO:
    {context}
    PREGUNTA:
    {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Eres un analista riguroso de llamadas telefónicas. Tu prioridad es precisión, no suposición."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content