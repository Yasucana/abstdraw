# abstdraw

`abstdraw.py` generates abstract line art inspired by Rafael Araujo.  It uses
the current date, the local weather (fetched from `wttr.in`), an energy level
digit, and a short text prompt.  These values determine a random seed so the art
is reproducible for the same inputs.  The drawing is displayed in a window using
golden ratio proportions.  The color of the lines is derived from the energy
digit, the text controls how chaotic the pattern becomes, and the energy level
also determines how many obstacle shapes are drawn on top of the art.

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

Run the script and follow the prompts for the energy level and words:

```bash
python abstdraw.py
```

The generated abstract art will open in a window.  If `tkinter` is unavailable
the program falls back to ASCII art output.  Colors vary with the energy level,
the diversity of the words adds more chaotic noise, and higher energy values
add more obstacle rectangles to the drawing.
