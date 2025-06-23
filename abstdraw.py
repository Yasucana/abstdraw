import datetime
import requests
import numpy as np


def simple_hash(text: str) -> int:
    """Return a 32-bit FNV-1a hash of the given text."""
    fnv_prime = 16777619
    hash_ = 2166136261
    for byte in text.encode("utf-8"):
        hash_ ^= byte
        hash_ = (hash_ * fnv_prime) % 2 ** 32
    return hash_


def draw_ascii(points, width: int = 60, height: int = 30) -> None:
    """Render points as ASCII art on the terminal."""
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for x, y in points:
        xi = min(width - 1, max(0, int(x * (width - 1))))
        yi = min(height - 1, max(0, int(y * (height - 1))))
        grid[height - 1 - yi][xi] = "*"
    for row in grid:
        print("".join(row))


def get_weather():
    """Return a string describing the local weather using wttr.in."""
    try:
        resp = requests.get("https://wttr.in/?format=j1", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data["current_condition"][0]["weatherDesc"][0]["value"]
    except Exception as exc:
        print("Weather lookup failed:", exc)
    return "Unknown"


def generate_art(feeling: int, words: str):
    date_str = datetime.date.today().strftime("%Y%m%d")
    weather = get_weather()

    seed_input = f"{date_str}-{weather}-{feeling}-{words}"
    seed = simple_hash(seed_input)
    rng = np.random.default_rng(seed)

    # generate chaotic sequence using logistic map
    x = rng.random()
    r = 4.0
    points = []
    for _ in range(5000):
        x = r * x * (1 - x)
        y = r * x * (1 - x)
        points.append((x, y))
    points = np.array(points)
    points += rng.normal(scale=0.1, size=points.shape)

    # normalize points to [0,1]
    points = (points - points.min(axis=0)) / (points.max(axis=0) - points.min(axis=0))

    print(f"{date_str} - {weather}\nFeeling: {feeling}\n{words}")
    draw_ascii(points)


def main():
    feeling = int(input("Feeling (1-100): "))
    words = input("Words (up to 100): ")[:100]
    generate_art(feeling, words)


if __name__ == "__main__":
    main()
