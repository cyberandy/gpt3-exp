import streamlit as st
import json
import openai
import yaml
import re

from pathlib import Path
from time import perf_counter
from typing import Dict
from openai.openai_object import OpenAIObject
from loguru import logger

PAGE_CONFIG = {
    "page_title":"GPT-3 for SEO by WordLift",
    "page_icon":"assets/fav-ico.png",
    "layout":"centered"
    }
st.set_page_config(**PAGE_CONFIG)

# Settings models and path
MODELS = ["davinci", "curie", "babbage", "ada"]
DATASET_PATH = Path(__file__).parents[1] / "gpt3_exp" / "datasets"
GPT3_CONFIG_PATH = Path(__file__).parents[1] / "gpt3_exp" / "gpt3_config.yml"
DATASETS = dict(
    [
        (re.sub(r"_", " ", str(ds).split("/")[-1].split(".yml")[0].title()), ds)
        for ds in list(DATASET_PATH.glob("*.yml"))
    ]
)
PARAMS = {}

# Experimentation - here is where everything happens
def experimentation() -> None:
    st.title("👾 GPT-3 Experimentation 👾")
    debug = st.sidebar.selectbox("Debug mode:", [False, True])
    select_option = st.sidebar.radio(
        "Set API key:", ["Add your own", "Load local config"]
    )
    if select_option == "Add your own":
        key_added = st.sidebar.text_area("Add OpenAI key *", max_chars=45)
        key_submit = st.sidebar.button("Submit key")
        if key_submit:
            openai.api_key = key_added
            st.write("(OpenAI key loaded)")
    elif select_option == "Load local config":
        load_local = st.sidebar.button("Load local config")
        if load_local:
            load_openai_key()
            st.write("(OpenAI key loaded)")

    # GPT-3 parameters
    PARAMS["engine"] = st.sidebar.selectbox("Select OpenAI model(`engine`):", MODELS)
    st.markdown(f"Model selected: `{PARAMS['engine']}`")

    PARAMS["max_tokens"] = st.sidebar.slider(
        "Max Tokens to generate(`max_tokens`):", min_value=1, max_value=2048, value=64, step=1
    )
    PARAMS["best_of"] = st.sidebar.slider(
        "Max number of completions(`best_of`):", min_value=1, max_value=2048, step=1
    )
    randomness = st.sidebar.radio("Randomness param:", ["temperature", "top_n"])
    if randomness == "temperature":
        PARAMS["temperature"] = st.sidebar.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.1
        )
    elif randomness == "top_n":
        PARAMS["top_p"] = st.sidebar.slider(
            "Top P (Alternative sampling to `temperature`)", min_value=0.0, max_value=1.0
        )

    PARAMS["stop"] = "\n"
    PARAMS["presence_penalty"] = st.sidebar.slider(
        "Presence penalty(`presence_penalty`)", min_value=0.0, max_value=1.0
    )
    PARAMS["frequency_penalty"] = st.sidebar.slider(
        "Frequency penalty(`frequence_penalty`)", min_value=0.0, max_value=1.0
    )

    dataset = []
    prime = st.selectbox("Select dataset:", list(DATASETS.keys()))
    dataset = load_primes(prime=prime)

    #elif prime_type == "Upload own":
    #    file_string = st.file_uploader("Upload dataset", type=["yaml", "yml"])
    #    dataset = yaml.safe_load(file_string)
    #    st.success("Uploaded successfully")
    prompt = st.text_area("Enter your prompt(`prompt`)", value="Enter just the text...")
    submit = st.button("Submit")
    stop = st.button("Stop request")
    parsed_primes = "".join(list(dataset["dataset"].values()))

    PARAMS[
        "prompt"
    ] = f"{parsed_primes}\n\n{dataset['input']}:{prompt}\n{dataset['output']}:"
    if debug:
        st.write(PARAMS)

    if submit:
        with st.spinner("Requesting completion..."):
            ts_start = perf_counter()
            request = openai.Completion.create(**PARAMS)
            ts_end = perf_counter()
        if debug:
            st.write(request)
        st.write([choice["text"] for choice in request["choices"]])
        st.error(f"Took {round(ts_end - ts_start, 3)} secs to get completion/s")
        
    if stop:
        st.error("Process stopped")
        st.stop()
    # except Exception as err:
    #     st.error(f"[ERROR]:: {err}")


def load_primes(prime: str) -> Dict:
    with open(DATASETS[prime], "r") as file_handle:
        dataset = yaml.safe_load(file_handle)
    return dataset


def load_openai_key() -> None:
    with open(GPT3_CONFIG_PATH, "r") as file_handle:
        openai.api_key = yaml.safe_load(file_handle)["GPT3_API"]

def main():
    # here comes the sidebar
    st.sidebar.image("assets/logo-wordlift.png", width=200)
    # here we load the core of the app
    experimentation()
    st.sidebar.subheader("About this demo")
    st.sidebar.info("The goal is to test all the possible SEO use-cases for GPT-3.")

if __name__ == "__main__":
    main()