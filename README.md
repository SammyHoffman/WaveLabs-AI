# 🎧 DJ Automation CLI

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Tests](https://github.com/Katazui/DJAutomation/actions/workflows/python-tests.yml/badge.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Katazui/DJAutomation.svg)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Katazui/DJAutomation.svg)
![GitHub Issues](https://img.shields.io/github/issues/Katazui/DJAutomation.svg)
![GitHub Contributors](https://img.shields.io/github/contributors/Katazui/DJAutomation.svg)
![GitHub Last Commit](https://img.shields.io/github/last-commit/Katazui/DJAutomation.svg)
![GitHub Issues Closed](https://img.shields.io/github/issues-closed/Katazui/DJAutomation.svg)
![GitHub Release](https://img.shields.io/github/release/Katazui/DJAutomation.svg)
![Repo Size](https://img.shields.io/github/repo-size/Katazui/DJAutomation.svg)
![GitHub Forks](https://img.shields.io/github/forks/Katazui/DJAutomation.svg?style=social&label=Fork)
![GitHub Stars](https://img.shields.io/github/stars/Katazui/DJAutomation.svg?style=social&label=Stars)

![DJ Automation Banner](https://katazui.com/wp-content/uploads/2023/07/Katazui-Logo-1-300x188.png)

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
    - [📌 Key Settings](#-key-settings)
  - [🚀 Installation](#-installation)
  - [🔧 Usage](#-usage)
    - [📥 Download Tracks](#-download-tracks)
    - [🎵 Upload to Mixcloud](#-upload-to-mixcloud)
    - [🧪 Run Tests](#-run-tests)
      - [Run All Tests:](#run-all-tests)
      - [Run Mixcloud Tests Only:](#run-mixcloud-tests-only)
- [🧪 Custom Testing](#-custom-testing)
  - [📚 Modules Overview](#-modules-overview)
    - [🔍 Download Module (modules/download/)](#-download-module-modulesdownload)
    - [☁️ Mixcloud Module (modules/mixcloud/)](#️-mixcloud-module-modulesmixcloud)
    - [🎨 Core Module (core/)](#-core-module-core)
    - [🛠️ Configuration (config/)](#️-configuration-config)
    - [🧪 Tests (tests/)](#-tests-tests)
- [🔒 Security](#-security)
- [📞 Support](#-support)
- [📝 License](#-license)
- [🙏 Contributing](#-contributing)

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
# .env
# Only store API keys or other sensitive credentials here.
# Example placeholders have been left blank. Fill in as needed.

# Mixcloud OAuth
MIXCLOUD_CLIENT_ID=""
MIXCLOUD_CLIENT_SECRET=""

# Spotify
SPOTIFY_CLIENT_ID=""
SPOTIFY_CLIENT_SECRET=""

# Last.fm
LASTFM_API_KEY=""

# Deezer
DEEZER_API_KEY=""

# MusicBrainz
MUSICBRAINZ_API_TOKEN=""
```

### 🛠️ config/settings.py

Centralized configuration file that imports environment variables and sets default values.

### 📌 Key Settings

• **Paths**: Directories for tracks, covers, finished uploads, etc.

• **API Credentials**: Client IDs and secrets for Mixcloud, Spotify, etc.

• **Upload Parameters**: Maximum uploads per run, publish times, and tags.

• **Toggles**: Enable or disable features like Mixcloud integration and color logs.

---

## 🚀 Installation

1. Clone the Repository:

   ```
   git clone https://github.com/Katazui/DJAutomation.git
   cd DJAutomation
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:

   • Create a `.env` file in the root directory.

   • Populate it with the necessary credentials and paths as shown in the **Configuration** section.

---

## 🔧 Usage

### 📥 Download Tracks

**_TODO_**

### 🎵 Upload to Mixcloud

**_TODO_**

### 🧪 Run Tests

Run all tests or specific ones (e.g. Mixcloud tests, Album Cover, Downloads, etc).

#### Run All Tests:

```
python cli/main.py test
```

#### Run Mixcloud Tests Only:

```
python cli/main.py test --mixcloud
```

---

# 🧪 Custom Testing

Ensure your codebase remains robust by running automated tests.

1. **Run Tests via CLI**:

```
python cli/main.py test
```

• **All Tests**: Executes all tests in the `tests/` directory.

• **Specific Tests**: Use flags like `--mixcloud` to run targeted tests.

2. **Run Tests Directly with Pytest**:

```
pytest tests/
```

3. **Adding New Tests**:

• Create new test files in the `tests/` directory following the `test_*.py` nameing convention.

• Ensure your tests cover different modukles and functionalities.

---

## 📚 Modules Overview

### 🔍 Download Module (modules/download/)

• `downloader.py`: Handles downloading audio tracks from provided links. Supports interactive and file-based modes.

• `post_process.py`: Organizes downloaded files into structured directories for easy management.

### ☁️ Mixcloud Module (modules/mixcloud/)

• `uploader.py`: Manages the uploading of tracks to Mixcloud, including handling OAuth authentication and file uploads.

• `scheduler.py`: (Future) Implements scheduling logic to automate upload timings.

• `cli.py`: Contains CLI-specific functions for Mixcloud integration.

### 🎨 Core Module (core/)

• `color_utils.py`: Provides utilities for color-coded messages in the CLI, enhancing readability and user experience.

### 🛠️ Configuration (config/)

• `settings.py`: Centralized configuration file importing environment variables and setting default values.

• `mixcloud/settings.py`: Mixcloud-specific configurations, including API credentials and upload parameters.

### 🧪 Tests (tests/)

• `test_mixcloud.py`: Contains unit and integration tests for the Mixcloud uploader module, ensuring reliability and correctness.

---

# 🔒 Security

• **Sensitive Data**: All sensitive credentials (API keys, secrets) are stored in the `.env` file and **never** committed to version control.

• `.gitignore`: Ensure your `.env` file is listed in `.gitignore` to prevent accidental exposure.

---

# 📞 Support

If you encouynter any issues or have questions, feel free to reach out:

• **Email**: FootLong@Duck.com

• **GitHub Issues:** [Open an Issue](https://github.com/Katazui/DJAutomation/issues/new/choose)

---

# 📝 License

This project is licensed under the [MIT](https://opensource.org/license/MIT) License. See the [LICENSE](https://github.com/Katazui/DJAutomation?tab=MIT-1-ov-file#) file for details.

---

# 🙏 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

1. **Fork the Repository.**

2. **Create a Feature Branch:**

```
git checkout -b feature/YourFeature
```

3. **Commit Your Changes:**

```
git commit -m "Add Your Feature Name"
```

4. **Push to the Branch**:

```
git push origin feature/YourFeature
```

5. **Open a Pull Request.**

---

Stay tuned for more features and improvements! Thank you for using DJ Automation CLI. 🎉
