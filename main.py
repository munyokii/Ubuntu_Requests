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
import hashlib
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

    def check_content_safety(self, response):
        """Checking if the response content is safe to download"""
        content_type = response.headers.get('content-type', '').lower()

        # Checking if its actually an image
        if not content_type.startswith('image/'):
            return False, f"Content is not an image (type: {content_type})"

        # Checking content length which limits to 50MB
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 50 * 1024 * 1024:
            return False, "Image too large (>50MB)"

        return True, "Safe to download"

    def calculate_content_hash(self, content):
        """Calculating image hash to detect duplicates"""
        return hashlib.sha256(content).hexdigest()

    def fetch_image(self, url):
        """Fetching a single image from URL with proper error handling"""
        print(f"Connecting to: {url}")

        try:
            # Making requests with timeout and stream for large files
            response = self.session.get(url, timeout=15, stream=True)
            response.raise_for_status()

            # Checking content safety
            is_safe, message = self.check_content_safety(response)
            if not is_safe:
                return False, f"Safety check failed: {message}"
            
            # Getting content
            content = response.content

            # Checking for duplicates
            content_hash = self.calculate_content_hash(content)
            if content_hash in self.downloaded_hashes:
                return False, "Duplicate image (already downloaded)"
            
            # Generating filename
            content_type = response.headers.get('content-type')
            filename = self.get_filename_from_url(url, content_type)
            filepath = os.path.join(self.directory, filename)

            # Handling filename conflicts
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1
            
            # Saving image
            with open(filepath, 'wb') as f:
              f.write(content)
            
            # Add the hash to prevent duplicates
            self.downloaded_hashes.add(content_hash)

            file_size = len(content) / 1024
            print(f"Successfully fetched: {os.path.basename(filepath)}")
            print(f"Image saved to {filepath} ({file_size:.1f} KB)")

            return True, filepath

        except requests.exceptions.Timeout:
            return False, "Connection timeout - the server took too long to respond"
        except requests.exceptions.ConnectionError:
            return False, "Connection failed - check your internet connection"
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False, "Image not found (404)"
            elif e.response.status_code == 403:
                return False, "Access forbidden (403) - server rejected the request"
            else:
                return False, f"HTTP error {e.response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {e}"
        except IOError as e:
            return False, f"File save error: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"