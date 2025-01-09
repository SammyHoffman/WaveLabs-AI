# 🎧 DJ Automation CLI

![DJ Automation Banner](https://your-image-link.com/banner.png)

Welcome to the **DJ Automation CLI**! This powerful tool streamlines your DJ workflow by automating tasks such as downloading tracks, organizing files, generating AI covers, and uploading mixes to Mixcloud. Whether you're managing a personal collection or handling large-scale uploads, this CLI has got you covered. 🚀

---

## 📜 Table of Contents

- [🎧 DJ Automation CLI](#-dj-automation-cli)
  - [📜 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🗂️ Project Structure](#️-project-structure)
  - [⚙️ Configuration](#️-configuration)
    - [📄 `.env` File](#-env-file)
      - [📌 Sample `.env`:](#-sample-env)
    - [🛠️ config/settings.py](#️-configsettingspy)
    - [📌 Key Settings:](#-key-settings)
  - [🚀 Installation](#-installation)
  - [📚 Modules Overview](#-modules-overview)

---

## ✨ Features

- **Automated Downloads**: Fetch audio tracks from various sources effortlessly.
- **File Organization**: Automatically organize your downloads for easy access.
- **AI Cover Generation**: (Coming Soon) Create stunning AI-generated covers for your mixes.
- **Mixcloud Integration**: Seamlessly upload your mixes to Mixcloud with OAuth authentication.
- **Scheduling**: Schedule uploads to publish your mixes at optimal times.
- **Robust Testing**: Ensure reliability with comprehensive automated tests.
- **Colorful CLI**: Enjoy an intuitive and visually appealing command-line interface with color-coded messages. 🎨

---

## 🗂️ Project Structure

```
DJAutomation/
│
├── cli/
│   ├── main.py              # Main CLI entry point
│   └── test_cli.py          # CLI for running tests
│
├── config/
│   ├── settings.py          # Configuration settings
│   └── mixcloud/
│       └── settings.py      # Mixcloud-specific configurations
│
├── core/
│   └── color_utils.py       # Utilities for colored CLI messages
│
├── modules/
│   ├── download/
│   │   ├── downloader.py    # Module for downloading tracks
│   │   └── post_process.py  # Module for organizing downloaded files
│   │
│   └── mixcloud/
│       ├── uploader.py      # Module for uploading to Mixcloud
│       ├── scheduler.py     # Module for scheduling uploads
│       └── cli.py           # CLI-specific functions for Mixcloud
│
├── tests/
│   └── test_mixcloud.py     # Tests for Mixcloud uploader
│
├── .env                     # Environment variables (not committed)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Configuration

### 📄 `.env` File

All sensitive credentials and environment-specific settings are managed through the `.env` file. **Ensure this file is listed in your `.gitignore` to prevent accidental commits of sensitive information.**

#### 📌 Sample `.env`:

```dotenv
# DJ Automation Configuration

# Mixcloud Credentials
MIXCLOUD_CLIENT_ID="your_mixcloud_client_id"
MIXCLOUD_CLIENT_SECRET="your_mixcloud_client_secret"

# Spotify Credentials
SPOTIFY_CLIENT_ID="your_spotify_client_id"
SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"

# Other API Keys
LASTFM_API_KEY="your_lastfm_api_key"
DEEZER_API_KEY="your_deezer_api_key"
MUSICBRAINZ_API_TOKEN="your_musicbrainz_api_token"

# Paths
DJ_POOL_BASE_PATH="/path/to/dj_pool"
LOCAL_TRACK_DIR="/path/to/local_tracks"
EXTERNAL_TRACK_DIR="/path/to/external_tracks"
COVER_IMAGE_DIRECTORY="/path/to/cover_images"
FINISHED_DIRECTORY="/path/to/finished_uploads"
TITLES_FILE="/path/to/titles.csv"
UPLOAD_LINKS_FILE="uploadLinks.txt"
PUBLISHED_DATES="/path/to/published_dates.txt"

# Upload Settings
MAX_UPLOADS=8
PUBLISHED_HOUR=12
PUBLISHED_MINUTE=00

# Toggles
USE_COLOR_LOGS=True
DEBUG_MODE=False
USE_EXTERNAL_TRACK_DIR=True
MIXCLOUD_ENABLED=True
MIXCLOUD_PRO_USER=True

# Server Settings
MIXCLOUD_PORT=8001
```

### 🛠️ config/settings.py

Centralized configuration file that imports environment variables and sets default values.

### 📌 Key Settings:

    •	Paths: Directories for tracks, covers, finished uploads, etc.
    •	API Credentials: Client IDs and secrets for Mixcloud, Spotify, etc.
    •	Upload Parameters: Maximum uploads per run, publish times, and tags.
    •	Toggles: Enable or disable features like Mixcloud integration and color logs.

---

## 🚀 Installation

1. Clone the Repository:

```
git clone https://github.com/yourusername/DJAutomation.git
cd DJAutomation
```
---

## 📚 Modules Overview

🔍 Download Module (modules/download/)
	•	downloader.py: Handles downloading audio tracks from provided links. Supports interactive and file-based modes.
	•	post_process.py: Organizes downloaded files into structured directories for easy management.

☁️ Mixcloud Module (modules/mixcloud/)
	•	uploader.py: Manages the uploading of tracks to Mixcloud, including handling OAuth authentication and file uploads.
	•	scheduler.py: (Future) Implements scheduling logic to automate upload timings.
	•	cli.py: Contains CLI-specific functions for Mixcloud integration.

🎨 Core Module (core/)
	•	color_utils.py: Provides utilities for color-coded messages in the CLI, enhancing readability and user experience.

🛠️ Configuration (config/)
	•	settings.py: Centralized configuration file importing environment variables and setting default values.
	•	mixcloud/settings.py: Mixcloud-specific configurations, including API credentials and upload parameters.

🧪 Tests (tests/)
	•	test_mixcloud.py: Contains unit and integration tests for the Mixcloud uploader module, ensuring reliability and correctness.