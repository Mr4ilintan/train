import csv
from dataclasses import dataclass
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


def get_profile_url() -> List[Everyone]:

    devto_profile_response = requests.get(f"https://dev.to/api/users/1")
    
    if devto_profile_response.status_code != 200:
       log.info(f"Got a {devto_profile_response.status_code} response from Dev.to.\n
       Reason: devto_profile_response.reason")
       abort()

    devs = code.json()

    partial_dev_data: List[Everyone] = []

    id: int = devs.get("id")
    username: str = devs.get("username")
    name: str = devs.get("name")
    twitter_username: str = devs.get("twitter_username")
    github_username: str = devs.get("github_username")
    location: str = devs.get("location")
    joined_at: Union[str, int] = devs.get("joined_at")
    profile_url: str = f"https://dev.to/{username}"

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
    if username:
        partial_dev_data.append(dev_to_be_parsed)

    #print(partial_dev_data)

    return partial_dev_data



def parse_devto_profiles(partial_developers: List[Everyone]):
    everyone = get_profile_url()
    for developer in partial_developers:
        profile_page = requests.get(everyone[0].profile_url)
        soup = BeautifulSoup(profile_page.text, 'lxml')

        meta = soup.find_all('div',{'class': ['key', 'value']})
        keys: List[str] = []
        values: List[str] = []
        for tag in meta:
            if tag.get("class") == ["key"]:
                keys.append(tag.text.strip().replace("\n", ""))
            elif tag.get("class") == ["value"]:
                values.append(tag.text.strip().replace("\n", ""))
        #print(keys)
        #print(values)

        socials = soup.find_all('a',{'target' : ['_blank']})

        social_info: Dict[str, str] = dict(zip(keys, values))

        links: List[str] = []
        for a in socials:
            links.append(a['href'])

        for link in links:
            if link.startswith("https://www.linkedin.com"):
                social_info['linked_in'] = link
            elif link.startswith('https://github.com'):
                social_info['github'] = link
            elif link.startswith('https://twitter.com'):
                social_info['twitter'] = link
            elif link.startswith('https://stackoverflow.com'):
                social_info['stack'] = link
            elif link.startswith('https://www.facebook.com'):
                social_info['facebook'] = link
            elif link.startswith('https://www.instagram.com'):
                social_info['instagram'] = link
            elif link.startswith('http://youtube.com'):
                social_info['youtube'] = link

        developer.email = social_info.get('email', '')
        developer.work = social_info.get('work', '')
        developer.education = social_info.get('education', '')
        developer.linked_in = social_info.get('linked_in', '')
        developer.twitter_url = social_info.get('twitter_url', '')
        developer.work_status = social_info.get('work_status','')
        developer.github_url = social_info.get('github_url','')
        developer.stackOverflow = social_info.get('stackOverflow','')
        developer.instagram = social_info.get('instagram','')
        developer.facebook = social_info.get('facebook','')
        developer.youtube = social_info.get('youtube','')



        save_dev_to_csv(entity=developer)


def save_dev_to_csv(entity: Everyone):
    with open("everyone_devto_profiles.csv", "a", newline="") as csvfile:
        fieldnames = [
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
            "id",
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
            "id",
            "linked_in",
            "stackOverflow",
            "instagram",
            "facebook",
            "youtube",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

if __name__ == '__main__':
    create_header()
    partial_profiles: List[Everyone] = get_profile_url()
    parse_devto_profiles(partial_profiles)
