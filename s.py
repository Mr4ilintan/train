import csv
import time
from dataclasses import dataclass
from os import abort
from typing import Optional, List, Union, Dict

import requests
from bs4 import BeautifulSoup

import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@dataclass
class Everyone:
    id: int
    profile_url: str
    username: Optional[str]
    name: Optional[str]
    github_username: Optional[str]
    twitter_username: Optional[str]
    location: Optional[str]
    joined_at: Optional[Union[str, int]]
    linked_in: Optional[str]
    email: Optional[str]
    work: Optional[str]
    stackOverflow: Optional[str]
    instagram: Optional[str]
    facebook: Optional[str]
    youtube: Optional[str]
    education: Optional[str]
    github_url: Optional[str]
    twitter_url: Optional[str]
    work_status: Optional[str]


def get_profile_url(current_id: int) -> Optional[Everyone]:

    devto_profile_response = requests.get(f"https://dev.to/api/users/{current_id}")

    accepted_status_codes = [200, 404]

    if devto_profile_response.status_code not in accepted_status_codes:
        log.info(
            f"Got a {devto_profile_response.status_code} response from Dev.to.\nReason: devto_profile_response.reason"
        )
        abort()

    if devto_profile_response.status_code == 404:
        return  # Skip this dev

    dev_json = devto_profile_response.json()

    id: int = dev_json.get("id", "")
    username: str = dev_json.get("username", "")
    name: str = dev_json.get("name", "")
    twitter_username: str = dev_json.get("twitter_username", "")
    github_username: str = dev_json.get("github_username", "")
    location: str = dev_json.get("location", "")
    joined_at: Union[str, int] = dev_json.get("joined_at", "")

    if username:
        profile_url: str = f"https://dev.to/{username}"
    else:
        log.info("No username")
        abort()

    dev_to_be_parsed: Everyone = Everyone(
        id=id,
        profile_url=profile_url,
        username=username,
        name=name,
        github_username=github_username,
        github_url="",
        twitter_url="",
        twitter_username=twitter_username,
        location=location,
        joined_at=joined_at,
        linked_in="",
        email="",
        work="",
        stackOverflow="",
        instagram="",
        facebook="",
        youtube="",
        education="",
        work_status="",
    )

    return dev_to_be_parsed


def parse_devto_profile(partial_developer: Optional[Everyone]):

    if partial_developer is None:  # In case developer is missing aka 404
        return

    profile_page = requests.get(partial_developer.profile_url)

    allowed_codes = [200, 404]

    if profile_page.status_code not in allowed_codes:
        log.info(f"Couldn't load profile page: {profile_page.status_code}")
        log.info(f"Reason: {profile_page.reason}")
        abort()

    soup = BeautifulSoup(profile_page.text, "lxml")

    meta = soup.find_all("div", {"class": ["key", "value"]})
    keys: List[str] = []
    values: List[str] = []
    for tag in meta:
        if tag.get("class") == ["key"]:
            keys.append(tag.text.strip().replace("\n", ""))
        elif tag.get("class") == ["value"]:
            values.append(tag.text.strip().replace("\n", ""))

    socials = soup.find_all("a", {"target": ["_blank"]})

    social_info: Dict[str, str] = dict(zip(keys, values))

    links: List[str] = []
    for a in socials:
        links.append(a["href"])

    for link in links:
        if link.startswith("https://www.linkedin.com"):
            social_info["linked_in"] = link
        elif link.startswith("https://github.com"):
            social_info["github"] = link
        elif link.startswith("https://twitter.com"):
            social_info["twitter"] = link
        elif link.startswith("https://stackoverflow.com"):
            social_info["stack"] = link
        elif link.startswith("https://www.facebook.com"):
            social_info["facebook"] = link
        elif link.startswith("https://www.instagram.com"):
            social_info["instagram"] = link
        elif link.startswith("http://youtube.com"):
            social_info["youtube"] = link

    partial_developer.email = social_info.get("email", "")
    partial_developer.work = social_info.get("work", "")
    partial_developer.education = social_info.get("education", "")
    partial_developer.linked_in = social_info.get("linked_in", "")
    partial_developer.twitter_url = social_info.get("twitter_url", "")
    partial_developer.work_status = social_info.get("work_status", "")
    partial_developer.github_url = social_info.get("github_url", "")
    partial_developer.stackOverflow = social_info.get("stackOverflow", "")
    partial_developer.instagram = social_info.get("instagram", "")
    partial_developer.facebook = social_info.get("facebook", "")
    partial_developer.youtube = social_info.get("youtube", "")

    save_dev_to_csv(entity=partial_developer)


def save_dev_to_csv(entity: Everyone):
    with open("everyone_devto_profiles.csv", "a", newline="") as csvfile:
        fieldnames = [
            "id",
            "email",
            "name",
            "username",
            "work",
            "location",
            "education",
            "joined",
            "twitter_username",
            "twitter_url",
            "work_status",
            "github_username",
            "github_url",
            "profile_url",
            "linked_in",
            "stackOverflow",
            "instagram",
            "facebook",
            "youtube",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(
            {
                "email": entity.email,
                "name": entity.name,
                "username": entity.username,
                "work": entity.work,
                "location": entity.location,
                "education": entity.education,
                "joined": entity.joined_at,
                "work_status": entity.work_status,
                "github_username": entity.github_username,
                "github_url": entity.github_url,
                "profile_url": entity.profile_url,
                "twitter_username": entity.twitter_username,
                "twitter_url": entity.twitter_url,
                "id": entity.id,
                "linked_in": entity.linked_in,
                "stackOverflow": entity.stackOverflow,
                "instagram": entity.instagram,
                "facebook": entity.facebook,
                "youtube": entity.youtube,
            }
        )


def create_header():
    with open("everyone_devto_profiles.csv", "w", newline="") as csvfile:
        fieldnames = [
            "id",
            "email",
            "name",
            "username",
            "work",
            "location",
            "education",
            "joined",
            "twitter_username",
            "twitter_url",
            "work_status",
            "github_username",
            "github_url",
            "profile_url",
            "linked_in",
            "stackOverflow",
            "instagram",
            "facebook",
            "youtube",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


if __name__ == "__main__":

    for i in range(9704, 400000):
        partial_profile: Everyone = get_profile_url(i)

        log.info(f"LAST ID: {i}")

        time.sleep(1)

        parse_devto_profile(partial_profile)
