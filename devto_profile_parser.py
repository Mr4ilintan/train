import csv
from typing import List, Dict
from bs4 import BeautifulSoup  # type: ignore
import requests
from model.developer import Developer


def save_dev_to_csv(entity: Developer):
    with open("devto_profiles.csv", "a", newline="") as csvfile:
        fieldnames = [
            "id",
            "profile_url",
            "username",
            "name",
            "github_username",
            "twitter_username",
            "location",
            "joined_at",
            "linked_in",
            "email",
            "work",
            "stackOverflow",
            "instagram",
            "facebook",
            "youtube",
            "education",
            "github_url",
            "twitter_url",
            "work_status",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(
            {
                "email": entity.email,
                "work": entity.work,
                "location": entity.location,
                "education": entity.education,
                "joined": entity.joined,
                "work_status": entity.work_status,
                "full_name": entity.full_name,
                "github_username": entity.github_username,
                "profile_url": entity.profile_url,
                # "id": entity.id
            }
        )


def create_header():
    with open("devto_profiles.csv", "w", newline="") as csvfile:
        fieldnames = [
            "email",
            "work",
            "location",
            "education",
            "joined",
            "work_status",
            "full_name",
            "github_username",
            "profile_url",
            # "id"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def parse_devto_profiles(partial_developers: List[Developer]) -> None:
    for developer in partial_developers:
        profile_page = requests.get(developer.profile_url)
        assert profile_page.status_code == 200
        soup = BeautifulSoup(profile_page.text, "lxml")

        meta = soup.find_all("div", {"class": ["key", "value"]})
        keys: List[str] = []
        values: List[str] = []
        for tag in meta:
            if tag.get("class") == ["key"]:
                keys.append(tag.text.strip().replace("\n", ""))
            elif tag.get("class") == ["value"]:
                values.append(tag.text.strip().replace("\n", ""))

        developer_info: Dict[str, str] = dict(zip(keys, values))

        developer.email = developer_info.get("email", "")
        developer.work = developer_info.get("work", "")
        developer.location = developer_info.get("location", "")
        developer.education = developer_info.get("education", "")
        developer.joined = developer_info.get("joined", "")
        developer.work_status = developer_info.get("work_status", "")

        save_dev_to_csv(entity=developer)
