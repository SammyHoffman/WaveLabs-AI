# 🎧 WaveLabs AI Agent

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Tests](https://github.com/Katazui/DJAutomation/actions/workflows/python-tests.yml/badge.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Katazui/DJAutomation.svg)
![Repo Size](https://img.shields.io/github/repo-size/Katazui/DJAutomation.svg)
![GitHub Release](https://img.shields.io/github/release/Katazui/DJAutomation.svg)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Donate-yellow.svg?style=flat)](https://buymeacoffee.com/katazui)
![GitHub Forks](https://img.shields.io/github/forks/Katazui/DJAutomation?style=social&label=Fork)
![GitHub Stars](https://img.shields.io/github/stars/Katazui/DJAutomation?style=social&label=Stars)


Welcome to the **WaveLabs AI DJ Agent**! An intelligent agent that creates seamless DJ sets by analyzing music characteristics and mixing tracks like a professional DJ. Whether you're managing a personal collection or handling large-scale uploads, WaveLabs has got you covered. 🚀

**LAST UPDATE 1/13/25: Documentation will be updated with the correct details. Many of the functions still work as intended.**


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
ai-dj-agent/
├── src/
│   ├── init.py
│   ├── agent.py          # Main AI DJ Agent implementation
│   ├── track.py          # Track data model
│   ├── analyzer.py       # Audio analysis functionality
│   └── utils.py          # Utility functions
├── tests/
│   ├── init.py
│   ├── test_agent.py
│   ├── test_track.py
│   ├── test_analyzer.py
│   └── test_utils.py
├── examples/
│   └── create_dj_set.py
├── docs/
│   ├── installation.md
│   ├── usage.md
│   └── api.md
├── requirements.txt
├── setup.py
├── LICENSE
├── README.md
└── .gitignore
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
# src/track.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Track:
    """Data model for a music track with its analyzed features."""
    
    path: str
    title: str
    bpm: float
    key: str
    energy: float
    duration: float
    genre: str
    
    # Additional optional metadata
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[int] = None
    
    @property
    def minutes(self) -> float:
        """Get track duration in minutes."""
        return self.duration / 60
    
    def is_compatible_key(self, other: 'Track') -> bool:
        """Check if this track is harmonically compatible with another track."""
        # TODO: Implement proper key compatibility logic
        return self.key == other.key
    
    def tempo_difference(self, other: 'Track') -> float:
        """Calculate the tempo difference with another track."""
        return abs(self.bpm - other.bpm)
    
    def energy_difference(self, other: 'Track') -> float:
        """Calculate the energy level difference with another track."""
        return abs(self.energy - other.energy)
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
# src/analyzer.py

import os
import librosa
import numpy as np
from typing import Tuple, Dict, Any
from deepseek import DeepSeekLLM
from .track import Track

class AudioAnalyzer:
    """Handles audio analysis using librosa and DeepSeek."""
    
    def __init__(self, model_name: str = "deepseek-coder", api_key: Optional[str] = None):
        self.llm = DeepSeekLLM(model_name=model_name, api_key=api_key)
    
    def analyze_file(self, file_path: str) -> Track:
        """
        Analyze an audio file and extract musical features.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Track object containing analyzed features
        """
        # Extract basic audio features
        basic_features = self._extract_basic_features(file_path)
        
        # Get advanced features using DeepSeek
        advanced_features = self._analyze_with_deepseek(file_path)
        
        # Combine all features
        return Track(
            path=file_path,
            title=os.path.basename(file_path),
            **basic_features,
            **advanced_features
        )
    
    def _extract_basic_features(self, file_path: str) -> Dict[str, Any]:
        """Extract basic audio features using librosa."""
        # Load audio file
        y, sr = librosa.load(file_path)
        
        # Extract features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Compute additional features
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        rms_energy = librosa.feature.rms(y=y)
        
        return {
            'bpm': float(tempo),
            'duration': duration,
            'spectral_centroid': np.mean(spectral_centroid),
            'rms_energy': np.mean(rms_energy)
        }
    
    def _analyze_with_deepseek(self, file_path: str) -> Dict[str, Any]:
        """Use DeepSeek to analyze advanced musical features."""
        prompt = f"""
        Analyze this audio track and provide:
        1. Musical genre
        2. Energy level (0-1)
        3. Musical key
        4. Additional characteristics
        Based on its acoustic features.
        """
        
        analysis = self.llm.generate(prompt)
        
        # TODO: Implement proper response parsing
        # This is a placeholder implementation
        return {
            'genre': 'electronic',
            'energy': 0.8,
            'key': 'Am'
        }
    
    def analyze_compatibility(self, track1: Track, track2: Track) -> float:
        """
        Analyze the mixing compatibility between two tracks.
        
        Returns:
            Compatibility score between 0 and 1
        """
        # Calculate various compatibility factors
        tempo_comp = 1 - (abs(track1.bpm - track2.bpm) / 20)  # Normalize BPM difference
        key_comp = 1.0 if track1.is_compatible_key(track2) else 0.0
        energy_comp = 1 - abs(track1.energy - track2.energy)
        
        # Weight the factors
        weights = {
            'tempo': 0.4,
            'key': 0.3,
            'energy': 0.3
        }
        
        # Calculate weighted score
        score = (
            tempo_comp * weights['tempo'] +
            key_comp * weights['key'] +
            energy_comp * weights['energy']
        )
        
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1
---
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-dj-agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered DJ agent using DeepSeek for music analysis and mixing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-dj-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-dj=src.cli:main",
        ],
    },
)
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

This project is licensed under the [MIT](https://opensource.org/license/MIT) License

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
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
*.mp3
*.wav
*.m4a
*.flac
.env
logs/
output/

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Distribution
.DS_Store
Thumbs.db
Stay tuned for more features and improvements! Thank you for using WaveLabs AI. 🎉
