import datetime
import math
import random

# プログラムは正常に動いています。描ける絵をもっと芸術的にしたいです。もっと抽象的な絵が描けるように純粋抽象絵画、新造形主義、アクション・ペインティング、カジミール・マレーヴィチ、カンディンスキー、などを学んで描けるようにしてください

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

COLOR_MAP = {
    0: "black",
    1: "blue",
    2: "red",
    3: "green",
    4: "purple",
    5: "orange",
    6: "brown",
    7: "darkcyan",
    8: "magenta",
    9: "gold",
}

try:
    import numpy as np
except Exception:
    np = None

try:
    import requests
except Exception:
    requests = None

try:
    import tkinter as tk
except Exception:
    tk = None


def simple_hash(text: str) -> int:
    fnv_prime = 16777619
    hash_ = 2166136261
    for byte in text.encode("utf-8"):
        hash_ ^= byte
        hash_ = (hash_ * fnv_prime) % 2 ** 32
    return hash_


def draw_window(points, energy_level, words, meaning, color, obstacles, max_lines=2000):
    if tk is None:
        draw_ascii(points, obstacles, max_lines=max_lines)
        return

    try:
        root = tk.Tk()
    except Exception:
        draw_ascii(points, obstacles)
        return

    phi = (1 + 5 ** 0.5) / 2
    width = 800
    height = int(width / phi)

    root.title("Abstract Energy Drawing")
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    prev = None
    for x, y in points[:max_lines]:
        xi = x * width
        yi = y * height
        if prev is not None:
            canvas.create_line(prev[0], prev[1], xi, yi, fill=color)
        prev = (xi, yi)

    rect_w = width
    rect_h = rect_w / phi
    x0, y0 = (width - rect_w) / 2, (height - rect_h) / 2
    for _ in range(6):
        x1 = x0 + rect_w
        y1 = y0 + rect_h
        canvas.create_rectangle(x0, y0, x1, y1, outline="blue")
        x0 += rect_w - rect_h
        rect_w, rect_h = rect_h, rect_w - rect_h

    for x0, y0, x1, y1 in obstacles:
        canvas.create_rectangle(x0 * width, y0 * height, x1 * width, y1 * height, outline="gray")

    text = f"Energy: {energy_level} - {meaning}"
    canvas.create_text(10, 10, anchor="nw", text=text, fill="darkgreen")
    canvas.create_text(10, 30, anchor="nw", text=words, fill="darkgreen")

    root.mainloop()


def draw_ascii(points, obstacles=None, width=60, height=30, max_lines=2000):
    if obstacles is None:
        obstacles = []
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for x, y in points[:max_lines]:
        xi = min(width - 1, max(0, int(x * (width - 1))))
        yi = min(height - 1, max(0, int(y * (height - 1))))
        grid[height - 1 - yi][xi] = "*"
    for x0, y0, x1, y1 in obstacles:
        for xi in range(int(x0 * (width - 1)), int(x1 * (width - 1)) + 1):
            for yi in range(int(y0 * (height - 1)), int(y1 * (height - 1)) + 1):
                if 0 <= xi < width and 0 <= yi < height:
                    grid[height - 1 - yi][xi] = "#"
    for row in grid:
        print("".join(row))


def get_weather() -> str:
    if not requests:
        return "Unknown"
    try:
        resp = requests.get("https://wttr.in/?format=j1", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data["current_condition"][0]["weatherDesc"][0]["value"]
    except Exception as exc:
        print("Weather lookup failed:", exc)
    return "Unknown"


def logistic_points(rng, chaos, count):
    x = rng.random()
    r = 3.5 + 0.5 * chaos
    pts = []
    for _ in range(count):
        x = r * x * (1 - x)
        y = r * x * (1 - x)
        pts.append((x, y))
    return pts


def neoplastic_points(rng, chaos, count):
    pts = []
    for _ in range(count // 10 + 1):
        if rng.random() < 0.5:
            y = rng.random()
            for _ in range(10):
                x = rng.random()
                pts.append((x, min(1.0, max(0.0, y + rng.uniform(-0.1, 0.1) * chaos))))
        else:
            x = rng.random()
            for _ in range(10):
                y = rng.random()
                pts.append((min(1.0, max(0.0, x + rng.uniform(-0.1, 0.1) * chaos)), y))
    return pts[:count]


def action_points(rng, chaos, count):
    x = rng.random()
    y = rng.random()
    pts = []
    for _ in range(count):
        x += rng.uniform(-0.2, 0.2) * (1 + chaos)
        y += rng.uniform(-0.2, 0.2) * (1 + chaos)
        pts.append((x, y))
    return pts


def kandinsky_points(rng, chaos, count):
    theta = rng.random() * 2 * math.pi
    r = 0.1
    pts = []
    for _ in range(count):
        theta += 0.1 + chaos * rng.random()
        r += 0.005 + chaos * rng.random() * 0.01
        pts.append((0.5 + r * math.cos(theta), 0.5 + r * math.sin(theta)))
    return pts


def generate_art(energy_level: int, words: str, style: str = "auto", max_lines: int = 1000) -> None:
    date_str = datetime.date.today().strftime("%Y%m%d")
    weather = get_weather()
    seed_input = f"{date_str}-{weather}-{energy_level}-{words}-{style}"
    seed = simple_hash(seed_input)

    if np is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = random.Random(seed)

    chaos = min(1.0, len(set(words.lower())) / 10)

    styles = {
        "logistic": logistic_points,
        "neoplastic": neoplastic_points,
        "action": action_points,
        "kandinsky": kandinsky_points,
    }

    if style == "auto":
        style = rng.choice(list(styles.keys())) if np is not None else random.choice(list(styles.keys()))

    points = styles.get(style, logistic_points)(rng, chaos, 5000)

    def noise():
        return rng.uniform(-(0.1 + 0.3 * chaos), 0.1 + 0.3 * chaos)

    points = [(x + noise(), y + noise()) for (x, y) in points]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    denom_x = max_x - min_x or 1.0
    denom_y = max_y - min_y or 1.0
    points = [((x - min_x) / denom_x, (y - min_y) / denom_y) for x, y in points]

    color = COLOR_MAP.get(energy_level % 10, "black")

    obstacles = []
    for _ in range(max(0, energy_level)):
        x0 = rng.random() * 0.9
        y0 = rng.random() * 0.9
        w = rng.random() * 0.1 + 0.02
        h = rng.random() * 0.1 + 0.02
        obstacles.append((x0, y0, min(1.0, x0 + w), min(1.0, y0 + h)))

    meaning = DIGIT_MEANINGS.get(energy_level % 10, "")
    print(f"{date_str} - {weather}\nEnergy level: {energy_level}\n{meaning}\n{words}")
    draw_window(points, energy_level, words, meaning, color, obstacles, max_lines=max_lines)


def main():
    energy = int(input("Energy level (0-9): "))
    words = input("Words (up to 100): ")[:100]
    try:
        max_lines = int(input("Number of lines (1-5000, default 1000): ") or 1000)
    except ValueError:
        max_lines = 1000
    max_lines = max(1, min(5000, max_lines))
    style = input("Style (logistic/neoplastic/action/kandinsky/auto): ") or "auto"
    generate_art(energy, words, style=style, max_lines=max_lines)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
