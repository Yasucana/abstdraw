# abstdraw

`abstdraw.py` generates chaotic abstract art based on the current date, the local
weather (fetched from `wttr.in`), a feeling value, and a short text prompt. The
combination of these inputs determines a random seed so the resulting art is
reproducible for the same inputs.

## Requirements

- Python 3 with `matplotlib`, `numpy` and `requests`

Install the dependencies with:

```bash
pip install matplotlib numpy requests
```

## Usage

Run the script and follow the prompts for the feeling value and words:

```bash
python abstdraw.py
```

A window with the generated abstract art will appear.
