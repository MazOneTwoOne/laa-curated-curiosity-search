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

this resource used to debug
https://docs.haystack.deepset.ai/docs/ollamagenerator


might need this for reading csv
```
pip install pandas
```