import datetime
import hashlib
import requests
import numpy as np
import matplotlib.pyplot as plt


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
    seed = int(hashlib.sha256(seed_input.encode()).hexdigest(), 16) % 2**32
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

    plt.figure(figsize=(8, 8))
    plt.scatter(points[:, 0], points[:, 1], c=np.linspace(0, 1, len(points)), cmap="hsv", alpha=0.6, s=10)
    plt.axis("off")
    plt.title(f"{date_str} - {weather}\nFeeling: {feeling}\n{words}")
    plt.show()


def main():
    feeling = int(input("Feeling (1-100): "))
    words = input("Words (up to 100): ")[:100]
    generate_art(feeling, words)


if __name__ == "__main__":
    main()
