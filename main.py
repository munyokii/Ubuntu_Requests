#!/usr/bin/env python3
"""
Ubuntu Image Fetcher
A tool for mindfully collecting images from the web

Embodies Ubuntu principles:
- Community: Connects to the wider web community
- Respect: Handles errors gracefully without crashing
- Sharing: Organizes fetched images for later sharing
- Practicality: Creates a tool that serves a real need
"""

import os
import requests


class UbuntuImageFetcher:
    """An image fetcher that embodies ubuntu principles"""
    def __init__(self, directory="Fetched_Images"):
        self.directory = directory
        self.downloaded_hashes = set()
        self.session = requests.Session()

        # Setting a user agent
        self.session.headers.update({
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Web Crawler)'
        })

    def create_directory(self):
        """Creating images directory if it doesn't exist"""
        try:
            os.makedirs(self.directory, exist_ok=True)
            return True
        except OSError as e:
            print(f"X Failed to create directory '{self.directory}': {e}")
            return False
