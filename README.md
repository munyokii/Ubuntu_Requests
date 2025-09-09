# Ubuntu Image Requests Downloader

"A person is a person through other persons." - Ubuntu Philosophy

A program that connects to the global community of the internet, respectfully fetches shared resources, and and download images.

## ✨ Features

### Core Functionality

- Single & Batch Downloads: Download one image or process multiple URLs
- Safety First: Content validation, size limits, and type checking
- Duplicate Prevention: SHA-256 content hashing prevents duplicate downloads
- Smart Organization: Automatic directory creation and file management
- URL Flexibility: Handles URLs with or without protocols

### Technical Features

- Timeout Protection: 15-second timeout prevents hanging connections
- Retry Logic: Built-in resilience for temporary network issues
- Progress Tracking: Clear feedback on download status
- Smart Naming: Intelligent filename generation from URLs or content types
- Memory Efficient: Streams large files to prevent memory issues

### User Experience

- Interactive Menu: Easy-to-use command-line interface
- Detailed Feedback: Comprehensive status messages and error reporting
- Ubuntu Branding: Consistent messaging that reflects Ubuntu values
- Accessibility: Clear, readable output suitable for screen readers

## Requirements
### System Requirements

- Python: 3.6 or higher
- Operating System: Windows, macOS, or Linux
- Internet Connection: Required for downloading images
- Disk Space: Varies based on images downloaded (default 50MB limit per image)

## Installation

### Clone Repository
```bash
  git clone https://github.com/munyokii/Ubuntu_Requests.git
```

### Change Directory
```bash
  cd Ubuntu_Requests
  ```

### Create virtual environment
```bash
  python -m venv <your-environment-name>
```

### Activate virtual environment
```bash
  <!-- On Windows -->
  <your-environment-name>\Scripts\activate

  <!-- On macOS/Linux -->
  source <your-environment-name>/bin/activate
```
### Install dependencies
```bash
  pip install -r requirements.txt
```

## Usage
### Basic Usage - Running the application
```bash
  python main.py
```
