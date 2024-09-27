import logging
from pathlib import Path
import requests
import requests.exceptions as requests_exception
import click
import pandas as pd
import json

logging.basicConfig(
    format="[%(asctime)-15s] %(levelname)s - %(message)s",
)


@click.command()
@click.option("--start_date", default="2024-09-27", type=click.DateTime())
def main(start_date):
    logging.info("Fetching Rocket data ...")

    fetch_rocket(start_date)


def fetch_rocket(start_date):
    url = "https://ll.thespacedevs.com/2.0.0/launch/upcoming"

    output_dir = Path("/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(output_dir, start_date + ".json")
    print(f"Output path: {output_path}")

    try:
        response = requests.get(url)
        data = response.json()

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except requests_exception.MissingSchema:
        print(f"{url} appears to be an invalid URL")
    except requests_exception.ConnectionError:
        print(f"Could not connect to {url}")


if __name__ == "__main__":
    main()
