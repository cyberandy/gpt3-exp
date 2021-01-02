# WordLift GPT-3: Experimentation tool for SEO

Code based on [Pratos](https://github.com/pratos/gpt3-exp)'s experimentation tool for GPT-3. 

![tool-gif](assets/tool-gpt3.gif)

__Note: You can read more on our [blog](https://wordlift.io/blog/en)__

This streamlit application is tool to experiment with GPT-3 in the context of SEO.

I made a small `streamlit` application that helps to manage it. Right now one can add `primes` or small datasets needed to prime the `Completion` API. This repo contains these `primes` in `src/gpt3_exp/datasets`.

## Setup

- Add your OpenAI key to `gpt3_exp/gpt3_config.yml` in this format:

```yaml
GPT3_API: ab-XXXXXXXXXXXXXXXXXXXXXXXX
```

- Or you can add it via the `streamlit` app directly.
- Install `poetry`. Follow the [official site](https://python-poetry.org/docs/#installation) or [this cookbook](https://soumendra.gitbook.io/deeplearning-cookbook/setting-up/setting-up-poetry-for-your-project)
- Once `poetry` is installed, run `poetry install`. This will download all the packages needed (ideally in `.venv`) as well as setup the repository.
- To run migrations: `poetry run migrate`

## Other Resources

- GPT3 Fine Tuning: [Github Link](https://github.com/cabhijith/GPT-3_Docs/blob/master/Fine-Tune.md)

PRs are welcomed. Would be happy to help out with any issues :)
