<p align="center">
  <img src="logo.png" alt="TechSage Logo" width="200">
</p>

# TechSage 🤖

TechSage is an advanced multi-agent LLM platform designed to deliver daily insights on technology, programming, architecture, and more. It utilizes both OpenAI's LLMs and local models via Ollama, ensuring flexibility and performance. Powered by CrewAI's multi-agent system, TechSage automates the retrieval of the latest trends and knowledge, keeping you informed and ahead in the tech world.

## Installation 🛠️

You can install TechSage via pip:

```bash
pip install git+https://github.com/VictorGoubet/techsage.git
```


## Prerequisites 💡 


- Python >=3.10,<=3.13
- `ollama` (if using a local model)
- OpenAI API key (if using a model from OpenAI or using crew memory)
- Delpha google search API key (if using API-based Google search)

## Setup ⚙️

Run the setup script to install additional dependencies and configure the environment:

```bash
setup-sage
```

- `--model <your-model-name>`: The name of the model you want to use (default is `llama3:8b`).

- `--verbose <1 or 0>`: The level of verbose you want (default is 0).

- `--local <True or False>`: Define if you want to use a local model with Ollama or an OpenAI API model (default is True).
- `--openai_api_key <key>`: Your openai api key. Required if you disabled local mode or if you want to use the crew memory (improve performance), you can also let this empty and export `OPENAI_API_KEY`.

- `--google_search_api_key <key>`: Your delpha google search api key. If empty a local google search will be perform, however, Google can quickly detect you and ban your IP. Note that only the Delpha Google Search API is supported. Feel free to modify the `api_google_search` method in `tools.py` if you want to use another API. You can also let this empty and export `GOOGLE_SEARCH_API_KEY`

## Launch 🚀

After setting up, launch the script:

```sh
launch-sage
```