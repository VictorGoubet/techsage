<p align="center">
  <img src="logo.png" alt="TechSage Logo" width="200">
</p>

# TechSage 🤖

TechSage is a simple multi-agent LLM platform designed to deliver daily insights on technology, programming, architecture, and more. It utilizes either OpenAI's LLMs or local models via Ollama, ensuring flexibility. Powered by CrewAI's multi-agent system, TechSage automates the retrieval of the latest trends and knowledge given a topic, keeping you informed and ahead in the tech world.



# Docker 🐋

You can install techsage using the provided docker image:

```bash
docker run -p 8501:8501 victorgoubet/techsage:latest
```

and go on 

```
http://localhost:8501
```

# Pip 📦


## Prerequisites 💡 

- Python >=3.10,<=3.13
- `ollama` (if using a local model) [install here](https://ollama.com/download/)

## Installation 🛠️

You can install TechSage via pip:

```bash
pip install git+https://github.com/VictorGoubet/techsage.git
```


## Configure [optional] ⚙️

Execute this command only if you want to use the shell interface and with specific configuration. If you plan to use the streamlit interface you can configure everything directly on it.

```bash
configure-sage
```

- `--model <your-model-name>`: The name of the model you want to use (default is `llama3:8b`).

- `--model_url <your-model-url>`: The api url of the model you want to use (default is `http://localhost:11434/v1`).

- `--verbose <1 or 0>`: The level of verbose you want during the configuration (default is 0).

- `--local <True or False>`: Define if you want to use a local model with Ollama or an OpenAI API model (default is True).

- `--openai_api_key <key>`: Your openai api key. Required if you disabled local mode or if you want to use the crew memory (improve performance).

- `--google_search_api_key <key>`: Your delpha google search api key. If empty a local google search will be perform, however, Google can quickly detect you and ban your IP. Note that only the Delpha Google Search API is supported. Feel free to modify the `api_google_search` method in `tools.py` if you want to use another API. A duckduckgo tool is also available so the agents may use this tools if something is not working with google.


## Launch 🚀

After setting up, launch the script, if you didn't configure anything it will perform the default configuration:

```sh
launch-sage
```

- `--streamlit <true or false>`: If True the streamlit interface will be used, otherwise a shell interface will appear