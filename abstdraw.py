import datetime
import random


# Mapping of digits to symbolic meanings used for the energy level.
# These phrases are derived from Rafael Araujo inspired numerology.
DIGIT_MEANINGS = {
    0: "Cycle - eternity, wholeness, or return",
    1: "Origin - singularity, identity, or will",
    2: "Duality - balance, opposition, or relationship",
    3: "Flow - growth, expression, or synthesis",
    4: "Structure - stability, foundation, or order",
    5: "Change - movement, adaptability, or life",
    6: "Harmony - beauty, compassion, or integration",
    7: "Mystery - insight, spirituality, or inner depth",
    8: "Power - infinity, mastery, or flow of energy",
    9: "Completion - fulfillment, culmination, or wisdom",
}

try:
    import numpy as np  # optional, used for generating points
except Exception:  # pragma: no cover - numpy may be missing
    np = None

try:
    import requests  # optional, used to fetch weather
except Exception:  # pragma: no cover - requests may be missing
    requests = None


def simple_hash(text: str) -> int:
    """Return a 32-bit FNV-1a hash of the given text."""
    fnv_prime = 16777619
    hash_ = 2166136261
    for byte in text.encode("utf-8"):
        hash_ ^= byte
        hash_ = (hash_ * fnv_prime) % 2 ** 32
    return hash_


try:
    import tkinter as tk  # pragma: no cover - GUI may be unavailable
except Exception:  # pragma: no cover - tkinter may be missing
    tk = None


def draw_window(points, energy_level: int, words: str, meaning: str) -> None:
    """Draw lines and golden rectangles on a Tkinter window."""
    if tk is None:  # fall back to ASCII art if tkinter is unavailable
        draw_ascii(points)
        return

    try:
        root = tk.Tk()
    except Exception:  # pragma: no cover - tk may fail in headless env
        draw_ascii(points)
        return

    phi = (1 + 5 ** 0.5) / 2
    width = 800
    height = int(width / phi)

    root.title("Abstract Energy Drawing")
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    prev = None
    for x, y in points[:2000]:
        xi = x * width
        yi = y * height
        if prev is not None:
            canvas.create_line(prev[0], prev[1], xi, yi, fill="black")
        prev = (xi, yi)

    # draw nested golden rectangles in a style reminiscent of Rafael Araujo
    rect_w = width
    rect_h = rect_w / phi
    x0, y0 = (width - rect_w) / 2, (height - rect_h) / 2
    for _ in range(6):
        x1 = x0 + rect_w
        y1 = y0 + rect_h
        canvas.create_rectangle(x0, y0, x1, y1, outline="blue")
        x0 += rect_w - rect_h
        rect_w, rect_h = rect_h, rect_w - rect_h

    text = f"Energy: {energy_level} - {meaning}"
    canvas.create_text(10, 10, anchor="nw", text=text, fill="darkgreen")
    canvas.create_text(10, 30, anchor="nw", text=words, fill="darkgreen")

    root.mainloop()


def draw_ascii(points, width: int = 60, height: int = 30) -> None:
    """Render points as ASCII art on the terminal."""
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for x, y in points:
        xi = min(width - 1, max(0, int(x * (width - 1))))
        yi = min(height - 1, max(0, int(y * (height - 1))))
        grid[height - 1 - yi][xi] = "*"
    for row in grid:
        print("".join(row))


def get_weather() -> str:
    """Return a string describing the local weather using wttr.in."""
    if not requests:
        # requests is optional; if missing, fall back to unknown weather
        return "Unknown"
    try:
        resp = requests.get("https://wttr.in/?format=j1", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data["current_condition"][0]["weatherDesc"][0]["value"]
    except Exception as exc:  # pragma: no cover - network may be unavailable
        print("Weather lookup failed:", exc)
    return "Unknown"


def generate_art(energy_level: int, words: str) -> None:
    """Generate and display deterministic art."""
    date_str = datetime.date.today().strftime("%Y%m%d")
    weather = get_weather()

    seed_input = f"{date_str}-{weather}-{energy_level}-{words}"
    seed = simple_hash(seed_input)

    if np is not None:
        rng = np.random.default_rng(seed)
        x = rng.random()
    else:
        rng = random.Random(seed)
        x = rng.random()

    r = 4.0
    points = []
    for _ in range(5000):
        x = r * x * (1 - x)
        y = r * x * (1 - x)
        points.append((x, y))

    if np is not None:
        points = np.array(points)
        points += rng.normal(scale=0.1, size=points.shape)
        # normalize points to [0,1]
        points = (
            points - points.min(axis=0)
        ) / (points.max(axis=0) - points.min(axis=0))
        points = points.tolist()
    else:
        def noise() -> float:
            return rng.uniform(-0.1, 0.1)

        points = [(x + noise(), y + noise()) for (x, y) in points]
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        denom_x = max_x - min_x or 1.0
        denom_y = max_y - min_y or 1.0
        points = [((x - min_x) / denom_x, (y - min_y) / denom_y) for x, y in points]

    meaning = DIGIT_MEANINGS.get(energy_level % 10, "")
    print(f"{date_str} - {weather}\nEnergy level: {energy_level}\n{meaning}\n{words}")
    draw_window(points, energy_level, words, meaning)


def main():
    energy = int(input("Energy level (0-9): "))
    words = input("Words (up to 100): ")[:100]
    generate_art(energy, words)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
