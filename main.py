from typing import List

from devto_profile_parser import create_header, parse_devto_profiles
from popular_devto_parser import get_devto_profile_urls

if __name__ == "__main__":
    create_header()
    profile_urls: List[str] = get_devto_profile_urls()
    parse_devto_profiles(profile_urls)
