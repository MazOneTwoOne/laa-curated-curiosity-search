## What is this?
- This a [RAG (Retrieval-Augmented Generation) application](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
- It uses [Haystack (by deepset)](https://haystack.deepset.ai/) as the Open Source AI Framework to orchestrate the tools
- The tools include:
  - an [LLM (ollama)](https://ollama.com/)
  - with a [model (mistral)](https://docs.mistral.ai/getting-started/models/)
  - to interrogate some data (https://huggingface.co/datasets/bilgeyucel/seven-wonders)
  - via a [UI (gradio)](https://www.gradio.app/)

## Setup
create local environment

```
brew install --cask miniconda
conda create -n haystack python=3.11 -y
conda init zsh
conda activate haystack
```

```
pip install haystack-ai datasets ollama-haystack gradio
```
download ollama to local machine - this is the LLM https://ollama.com/download 


use ollama to download the mistral model
```
ollama run mistral 
```

run the app
```
python app.py
```

might need this for reading csv
```
pip install pandas
```

## Resources
- https://mer.vin/2024/01/haystack-ai-to-create-rag-pipeline/
- https://aws.amazon.com/what-is/retrieval-augmented-generation/
- https://docs.haystack.deepset.ai/docs/ollamagenerator this resource used to debug