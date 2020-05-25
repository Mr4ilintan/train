from typing import List

import requests

from devto_profile_parser import Developer


def get_devto_profile_urls() -> List[Developer]:

    response = requests.get("https://dev.to/api/articles?top=50")

    developers = response.json()
    partial_developer_data: List[Developer] = []

    for developer in developers:
        data = developer.get("user")

        username: str = data.get("username")
        full_name: str = data.get("name")
        github_username: str = data.get("github_username")
        profile_url: str = f"https://dev.to/{username}"

        developer_to_be_parsed: Developer = Developer(
            username=username,
            full_name=full_name,
            github_username=github_username,
            profile_url=profile_url,
            email="",
            work="",
            location="",
            education="",
            joined="",
            work_status="",
        )
        if username:
            partial_developer_data.append(developer_to_be_parsed)

    return partial_developer_data
