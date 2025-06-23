# abstdraw

`abstdraw.py` generates chaotic abstract art based on the current date, the local
weather (fetched from `wttr.in`), a feeling value, and a short text prompt. The
combination of these inputs determines a random seed so the resulting art is
reproducible for the same inputs.

## Requirements

The script only needs Python 3. It optionally uses `numpy` and `requests` for
faster point generation and fetching the current weather. If these packages are
not available the program will still run, but the art will be generated using
Python's built in random module and the weather will be reported as "Unknown".

To enable the optional features install the extra packages:

```bash
pip install numpy requests
```

## Usage

Run the script and follow the prompts for the feeling value and words:

```bash
python abstdraw.py
```

The generated abstract art will be displayed as ASCII art in the terminal.
