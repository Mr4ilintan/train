from typing import List

from devto_profile_parser import create_header, parse_devto_profiles, Developer
from popular_devto_parser import get_devto_profile_urls

if __name__ == "__main__":
    create_header()
    partial_profiles: List[Developer] = get_devto_profile_urls()
    parse_devto_profiles(partial_profiles)
