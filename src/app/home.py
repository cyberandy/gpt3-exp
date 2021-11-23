# -*- coding: utf-8 -*-
"""
Updated on Tue Nov 23 2021

@author: Andrea Volpini
"""

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
from Interface import *

# Adding st page configuration
PAGE_CONFIG = {
    "page_title":"GPT-3 for SEO by WordLift",
    "page_icon":"assets/fav-ico.png",
    "layout":"wide"}

st.set_page_config(**PAGE_CONFIG)

local_css("assets/style.css")

# Settings models and path
MODELS = ["davinci", "curie", "babbage", "ada"]
DATASET_PATH = Path(__file__).parents[1] / "gpt3_exp" / "datasets"
DATASETS = dict(
    [
        (re.sub(r"_", " ", str(ds).split("/")[-1].split(".yml")[0].title()), ds)
        for ds in list(DATASET_PATH.glob("*.yml"))
    ]
)
PARAMS = {}

# Experimentation - here is where everything happens
def experimentation() -> None:
    # Sidebar (logo, key and model selection)
    st.sidebar.image("assets/logo-wordlift.png")
    key_added = st.sidebar.text_area("Add OpenAI key *", max_chars=55)
    key_submit = st.sidebar.button("Submit key")
    if key_submit:
        openai.api_key = key_added
        st.write("(OpenAI key loaded)")
        st.balloons()
    PARAMS["engine"] = st.sidebar.selectbox("Select OpenAI model:", MODELS)
    st.sidebar.subheader("About this app")
    st.sidebar.info("The goal is to test all the possible SEO use-cases for GPT-3.")
    st.sidebar.info(" Learn more about our [solutions for SEO automation](https://wordlift.io/enterprise-seo-platform/).")

    # Main screen layout
    col1, col2 = st.columns([3, 1])

    # Left Column (col1)
    col1.title("GPT-3 for SEO 🖋")
    col1.markdown(f"Model selected: `{PARAMS['engine']}`")

    dataset = []
    prime = col1.selectbox("Select the use-case:", list(DATASETS.keys()))
    dataset = load_primes(prime=prime)

    prompt = col1.text_area("Enter your prompt 👇", value=dataset['description'])
    submit = col1.button("Submit request")

    parsed_primes = "".join(list(dataset["dataset"].values()))

    PARAMS[
        "prompt"
    ] = f"{parsed_primes}\n\n{dataset['input']}:{prompt}\n{dataset['output']}:"

    # Right Column (col2) GPT-3 parameters
    PARAMS["max_tokens"] = col2.slider(
        "Max Tokens to generate:", min_value=1, max_value=2048, value=64, step=25
    )
    PARAMS["best_of"] = col2.slider(
        "Max number of completions:", min_value=1, max_value=2048, step=1
    )
    randomness = col2.radio("Randomness param:", ["temperature", "top_n"])
    if randomness == "temperature":
        PARAMS["temperature"] = col2.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.1
        )
    elif randomness == "top_n":
        PARAMS["top_p"] = col2.slider(
            "Top P (Alternative sampling to `temperature`)", min_value=0.0, max_value=1.0
        )

    PARAMS["stop"] = "\n"
    PARAMS["presence_penalty"] = col2.slider(
        "Presence penalty:", min_value=0.0, max_value=1.0
    )
    PARAMS["frequency_penalty"] = col2.slider(
        "Frequency penalty:", min_value=0.0, max_value=1.0
    )

    # Debug option
    debug = st.sidebar.selectbox("Debug mode:", [False, True])
    if debug:
        col1.write(PARAMS)

    if submit:
        with st.spinner("Requesting completion..."):
            ts_start = perf_counter()
            request = openai.Completion.create(**PARAMS)
            ts_end = perf_counter()
        if debug:
            col1.write(request)
        col1.write([choice["text"] for choice in request["choices"]])
        col1.error(f"Took {round(ts_end - ts_start, 3)} secs to get completion/s")

# Load dataset
def load_primes(prime: str) -> Dict:
    with open(DATASETS[prime], "r") as file_handle:
        dataset = yaml.safe_load(file_handle)
    return dataset

def main():
    # here we load the core of the app
    experimentation()

if __name__ == "__main__":
    main()