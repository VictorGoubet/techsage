import json
import os
import subprocess
import sys
from pprint import pprint
from typing import Optional

import click

from techsage.utils.constants import APP_FOLDER

VERBOSE = 0


def create_app_folder() -> None:
    """Create the folder of techsage if not existing"""
    os.makedirs(APP_FOLDER, exist_ok=True)
    os.makedirs(f"{APP_FOLDER}/models", exist_ok=True)


def check_ollama_installed() -> None:
    """
    Check if 'ollama' is installed.

    :raises subprocess.CalledProcessError: If the command to check 'ollama' fails.
    :raises FileNotFoundError: If 'ollama' is not found.
    """
    try:
        output = None if VERBOSE else subprocess.DEVNULL
        subprocess.check_output(["ollama", "--version"], stderr=output)
        print(" ✅ Ollama is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(" ❌ 'ollama' is not installed. Please install it first.")
        sys.exit(1)


def pull_model(model_name: str) -> None:
    """
    Pull a model using ollama.

    :param str model_name: The name of the model to pull.
    :raises subprocess.CalledProcessError: If the command to pull the model fails.
    """
    try:
        output = None if VERBOSE else subprocess.DEVNULL
        subprocess.check_call(
            ["ollama", "pull", model_name],
            stdout=output,
            stderr=output,
        )
        print(" ✅ Base model is ready")
    except subprocess.CalledProcessError as e:
        print(f" ❌ Failed to pull model {model_name}: {e}")
        sys.exit(1)


def create_model(new_model_name: str, config_file_path: str) -> str:
    """
    Create a new model using ollama.

    :param str new_model_name: The name of the new model to create.
    :param str config_file_path: The path where to find the configuration file of the custom model.
    :raises subprocess.CalledProcessError: If the command to create the model fails.
    :return str: The model of the created custom model.
    """
    try:
        output = None if VERBOSE else subprocess.DEVNULL
        subprocess.check_call(
            ["ollama", "create", new_model_name, "-f", config_file_path],
            stdout=output,
            stderr=output,
        )
        print(f" ✅ Custom model {new_model_name} is ready")
        return new_model_name
    except subprocess.CalledProcessError as e:
        print(f" ❌ Failed to create model {new_model_name}: {e}")
        sys.exit(1)


def create_model_file(model_name: str, folder_path: str) -> str:
    """
    Create a model configuration file with the given model name.

    :param str model_name: The name of the model to use in the configuration file.
    :param str folder_path: The path of the folder where the configuration file will be created.
    :return str: The path where to find the created model file.
    """
    config_content = f'FROM {model_name}\nPARAMETER temperature 0.8\nPARAMETER stop Result\nSYSTEM """"""'
    try:
        path_model_name = model_name.replace(":", "").replace("/", "")
        file_path = f"{folder_path}/{path_model_name}_Modelfile".replace("//", "/")
        with open(file_path, "w") as file:
            file.write(config_content)
        print(f" ✅ Model configuration file created at {file_path}")
        return file_path
    except Exception as e:
        print(f" ❌ Failed to create model configuration file: {e}")
        sys.exit(1)


def fallback_on_env(value: str, env_name: str) -> Optional[str]:
    """Return the value if not None, otherwise try to use the environement value

    :param str value: The value to check for
    :param str env_name: The name of the environment variable containing the fallback value
    :return Optional[str]: The processed value
    """
    if value is None or str(value).lower().strip() in ["none", "", "na"]:
        value = os.environ.get(env_name, "NA")
    return value


def save_config(
    model_name: str,
    openai_api_key: str,
    google_search_api_key: str,
    local: bool,
    model_url: Optional[str] = None,
) -> None:
    """Save the current configuration

    :param str model_name: The name of the crewai model.
    :param str openai_api_key: The api key of open ai to use
    :param str google_search_api_key: The delpha google search api key
    :param bool local: Flag indicating if the model is local or from OpenAI API.
    :param Optional[str] model_url: The api url of the model, default based on local
    """
    openai_api_key = fallback_on_env(openai_api_key, "OPENAI_API_KEY")
    google_search_api_key = fallback_on_env(google_search_api_key, "GOOGLE_SEARCH_API_KEY")

    if not local and openai_api_key == "":
        print(" ❌ OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    config = {
        "LOCAL": str(local).lower(),
        "OPENAI_API_BASE": model_url if model_url else "http://localhost:11434/v1" if local else "",
        "OPENAI_MODEL_NAME": model_name,
        "OPENAI_API_KEY": openai_api_key,
        "GOOGLE_SEARCH_API_KEY": google_search_api_key,
    }
    with open(f"{APP_FOLDER}/config.json", "w") as f:
        json.dump(config, f)
    print(f" ✅ Configuration saved in {APP_FOLDER}")
    if VERBOSE:
        pprint(config)
    return config


def configure(
    model: str,
    openai_api_key: str,
    google_search_api_key: str,
    local: str,
    verbose: int,
    model_url: Optional[str] = None,
) -> None:
    """
    Main function to orchestrate the configuration process: installing dependencies,
    checking if ollama is installed, pulling a model, and creating a new model.

    :param str model: The name of the local model to use.
    :param str openai_api_key: The openai key to use (for llm if not local and/or for memory mode), default local mode
    :param str google_search_api_key: The delpha google search api key (if api google search mode), default local mode
    :param str local: Flag indicating if the model is local or from OpenAI API.
    :param int verbose: 0 if no verbose 1 otherwise
    :param Optional[str] model_url: The api url of the model, default based on local
    """
    global VERBOSE
    VERBOSE = verbose
    local = str(local).lower().strip() == "true"
    print(" ⚙️ Configuration started..")
    create_app_folder()
    if local:
        check_ollama_installed()
        model_config_file_path = create_model_file(model, f"{APP_FOLDER}/models/")
        pull_model(model)
        crewai_model_name = create_model(f"{model}_crewai", model_config_file_path)
    else:
        crewai_model_name = model
    save_config(crewai_model_name, openai_api_key, google_search_api_key, local, model_url)


@click.command()
@click.option("--model", "-m", default="llama3:8b", help="The name of the model you want to use")
@click.option("--openai_api_key", "-oak", default="", help="Your openai api key")
@click.option("--google_search_api_key", "-gsak", default="", help="Your delpha google search api key")
@click.option(
    "--local",
    "-l",
    default="true",
    help="Set to True if using a local model with ollama, False for OpenAI API model",
)
@click.option("--verbose", "-v", default=0, help="0 to not see configuration details, 1 otherwise")
@click.option("--model_url", "-mu", default=None, help="The api url of the model")
def main(
    model: str,
    openai_api_key: str,
    google_search_api_key: str,
    local: str,
    verbose: int,
    model_url: Optional[str] = None,
) -> None:
    configure(model, openai_api_key, google_search_api_key, local, verbose, model_url)
