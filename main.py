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
import time
import mimetypes
from urllib.parse import urlparse

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

    def validate_url(self, url):
        """Validating and cleaning URL"""
        if not url.strip():
            return None, "URL cannot be empty"

        # Adding protocol if it is missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return None, "Invalid URL format"
            return url, None
        except ValueError as e:
            return None, f"URL parsing error: {e}"

    def get_filename_from_url(self, url, content_type=None):
        """Extracting or generating appropriate filename from URL"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # if no filename in URL, generate one based on content type
        if not filename or '.' not in filename:
            timestamp = int(time.time())

            if content_type:
                # Getting extension from content type
                extension = mimetypes.guess_extension(content_type.split(';')[0])
                if extension:
                    filename = f"image_{timestamp}{extension}"
                else:
                    filename = f"image_{timestamp}.jpg"
            else:
                filename = f"image_{timestamp}.jpg"

        filename = "".join(c for c in filename if c.isalnum() or c in '.-_')

        return filename