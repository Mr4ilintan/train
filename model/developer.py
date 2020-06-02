from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Developer:
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
