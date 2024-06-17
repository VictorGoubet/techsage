<p align="center">
  <img src="assets/logo.png" alt="TechSage Logo" width="200">
</p>

<h1 align="center">TechSage 🤖</h1>

<p align="center">
  TechSage is a multi-agent LLM platform delivering daily insights on technology, programming, cloud architecture, and more. Utilize OpenAI's LLMs or local models via Ollama, powered by CrewAI's multi-agent system, to stay ahead in the tech world.
</p>

<p align="center">
  <a href="#prerequisites-">Prerequisites</a> •
  <a href="#installation-%EF%B8%8F">Installation</a> •
  <a href="#configure-optional-%EF%B8%8F">Configure</a> •
  <a href="#launch-">Launch</a> •
  <a href="#docker-">Docker</a>
</p>

<br>

## Prerequisites 💡

- Python >= 3.10, <= 3.13
- `ollama` (if using a local model) [install here](https://ollama.com/download/)
- May need to install the c++ build tool if you don't already have it

## Installation 🛠️

To install TechSage, run:

```bash
pip install https://github.com/VictorGoubet/techsage/archive/refs/tags/v1.tar.gz
```

*Replace `v1` with the release you want to use.*

## Configure [optional] ⚙️

Execute this command only if you want to use the shell interface with specific configuration. For the Streamlit interface, you can configure everything directly within it.

```bash
configure-sage
```

### Configuration Options:

- `--model <your-model-name>`: Name of the model to use (default: `llama3:8b`).
- `--model_url <your-model-url>`: API URL of the model to use (default: `http://localhost:11434/v1`).
- `--verbose <1 or 0>`: Verbose level during configuration (default: 0).
- `--local <True or False>`: Use a local model with Ollama or an OpenAI API model (default: True).
- `--openai_api_key <key>`: Your OpenAI API key (required if local mode is disabled or using crew memory).
- `--google_search_api_key <key>`: Delpha Google Search API key. If empty, a local Google search will be performed. Modify `api_google_search` method in `tools.py` to use another API. A DuckDuckGo tool is also available.

## Launch 🚀

After setting up, launch the script with admin rights. If no configuration is provided, the default configuration will be used:

```sh
launch-sage
```

### Launch Options:

- `--streamlit <true or false>`: If `true`, the Streamlit interface will be used; otherwise, a shell interface will appear.

<br>

## Docker 🐋

Lazy to setup everything ? Just use the dedicated docker image and go to [http://localhost:8501](http://localhost:8501)

### CPU only

```bash
docker run -d -v ollama:/root/.ollama -p 8501:8501 victorgoubet/techsage:latest
```

### Nvidia GPU

First install GPU drivers for docker:

- **Linux**: [NVIDIA Container Toolkit⁠](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation).  
- **Windows**: [Nvidia Cuda on WSL](https://learn.microsoft.com/fr-fr/windows/ai/directml/gpu-cuda-in-wsl)  
- **Mac**: *Not supported*  

```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 8501:8501 victorgoubet/techsage:latest
```

*Note: GPU version not really stable* 

<br><br>

## App preview

<br>

<p align="center">
  <img src="assets/app.png" alt="Techsage app">
</p>


---
