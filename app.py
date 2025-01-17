# Importing required libraries
from datasets import load_dataset
from haystack import Document, Pipeline

# store and retreive data
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.generators.ollama import OllamaGenerator

# This is to visualise the dataset
import gradio as gr

import csv


with open('csv_dataset/L&D_Reviews.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)   
    dataset = [
        {
            "content": row["review"] + " " + row["\ufeffname"] + " " + row["url"] + " " + row["cost"] + " " + row["length"],
            "meta": {'url': row["url"], 'rating': row["rating"],}
        } for row in reader
    ]  
docs = [Document(**doc, id_hash_keys=["content", "meta"]) for doc in dataset]

# Initialize document store and write documents
document_store = InMemoryDocumentStore()
document_store.write_documents(docs)

# Initialize retriever
retriever = InMemoryBM25Retriever(document_store)

# Define prompt template
template = """
Given the following information, answer the question.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
"""

# Initialize prompt builder
prompt_builder = PromptBuilder(template=template)

# Initialize Ollama generator
generator = OllamaGenerator(
    model="mistral",
    url = "http://localhost:11434/api/generate",
    generation_kwargs={
        "num_predict": 100,
        "temperature": 0.9,
    }
)

# Create and configure pipeline
basic_rag_pipeline = Pipeline()
basic_rag_pipeline.add_component("retriever", retriever)
basic_rag_pipeline.add_component("prompt_builder", prompt_builder)
basic_rag_pipeline.add_component("llm", generator)
basic_rag_pipeline.connect("retriever", "prompt_builder.documents")
basic_rag_pipeline.connect("prompt_builder", "llm")

# Define function to run pipeline with Gradio
def ask_question(question):
    response = basic_rag_pipeline.run(
        {
            "retriever": {"query": question}, 
            "prompt_builder": {"question": question}
        }
    )
    return response["llm"]["replies"][0]


css = 'gradio.scss'

# Create Gradio interface
gr_interface = gr.Interface(
    fn=ask_question,
    inputs=gr.components.Textbox(lines=3, placeholder="Type to Explore"),
    outputs=gr.components.Textbox(lines=6),
    clear_btn=gr.ClearButton(visible=False),
    title="'Explore' component",
    submit_btn="Explore",
    allow_flagging="never",
    description="This a [RAG (Retrieval-Augmented Generation) application](https://aws.amazon.com/what-is/retrieval-augmented-generation/). It uses [Haystack (by deepset)](https://haystack.deepset.ai/) as the Open Source AI Framework to orchestrate the tools. The tools include: a way to manange our [LLM (olllama)](https://ollama.com/); with a [LLM model (mistral)](https://docs.mistral.ai/getting-started/models/); to interrogate some data (a CSV file, in this case); via a [UI (gradio)](https://www.gradio.app/).",
    css=css
)

gr_interface.launch(allowed_paths=["assets/fonts/light-f591b13f7d-v2.woff"])