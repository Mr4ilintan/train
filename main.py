from typing import Optional
import requests
import csv
from dataclasses import dataclass
import io


@dataclass
class Developer:
    full_name: Optional[str]
    username: Optional[str]
    github_url: Optional[str]


def save_dev_to_csv(entity: Developer):
    with io.open("result.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["full_name", "username", "github_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(
            {
                "full_name": entity.full_name,
                "username": entity.username,
                "github_url": entity.github_url,
            }
        )


def parse_devto_developers():
    with io.open("result.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["full_name", "username", "github_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

    response = requests.get("https://dev.to/api/articles?top=50")

    developers = response.json()

    for developer in developers:
        data = developer.get("user")
        print(data)
        entity: Developer = Developer(
            full_name=data.get("name", ""),
            username=data.get("username", ""),
            github_url=data.get("github_username", ""),
        )

        save_dev_to_csv(entity)


if __name__ == "__main__":
    # working on kekw
    response = requests.get("https://dev.to/api/articles?top=50")
    username_json = response.json()
    usernaame = username_json[0].get("user").get("username")
    links = requests.get(f"https://dev.to/{usernaame}")

    print(links)
