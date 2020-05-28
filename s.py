from dataclasses import dataclass
from typing import Optional, List, Union

import requests
from bs4 import BeautifulSoup

"""for ids in range(0, 15):
    ids = ids+1

code = requests.get(f'https://dev.to/api/users/{ids}')

a = code.json()"""


@dataclass
class Everyone:
    id: int
    profile_url: str
    username: Optional[str]
    name: Optional[str]
    github_username: Optional[str]
    twitter_username: Optional[str]
    website_url: Optional[str]
    location: Optional[str]
    joined_at: Optional[Union[str, int]]
    linked_in: Optional[str]
    twitch: Optional[str]
    email: Optional[str]
    work: Optional[str]
    stackOverflow: Optional[str]
    medium: Optional[str]
    instagram: Optional[str]
    dribbble: Optional[str]
    facebook: Optional[str]
    youtube: Optional[str]
    mastodon: Optional[str]
    gitlab: Optional[str]


def get_profile_url() -> List[Everyone]:

    code = requests.get(f"https://dev.to/api/users/1")

    print(code)

    devs = code.json()

    partial_dev_data: List[Everyone] = []

    id: int = devs.get("id")
    username: str = devs.get("username")
    name: str = devs.get("name")
    twitter_username: str = devs.get("twitter_username")
    github_username: str = devs.get("github_username")
    website_url: str = devs.get("website_url")
    location: str = devs.get("location")
    joined_at: Union[str, int] = devs.get("joined_at")
    profile_url: str = f"https://dev.to/api/users/1"

    dev_to_be_parsed: Everyone = Everyone(
        id=id,
        profile_url=profile_url,
        username=username,
        name=name,
        github_username=github_username,
        twitter_username=twitter_username,
        website_url=website_url,
        location=location,
        joined_at=joined_at,
        linked_in="",
        twitch="",
        email="",
        work="",
        stackOverflow="",
        medium="",
        instagram="",
        dribbble="",
        facebook="",
        youtube="",
        mastodon="",
        gitlab="",
    )
    if username:
        partial_dev_data.append(dev_to_be_parsed)

    print(partial_dev_data)

    return partial_dev_data

    # def parse_devto_profiles(partial_developers: List[Everyone]):


get_profile_url()


"""    for developer in partial_developers:
        profile_page = requests.get(developer.profile_url)
        soup = BeautifulSoup(profile_page.text, 'lxml')

        meta = soup.find_all('div',{'class': ['key', 'value']})
        print[meta]"""

# parse_devto_profiles()
