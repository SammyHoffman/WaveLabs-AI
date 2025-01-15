from setuptools import setup, find_packages
import os
import re

def parse_requirements(filename):
    """
    Parse a requirements file to load dependencies.
    Skips empty lines and comments.
    """
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Load dependencies from requirements.txt
install_requires = parse_requirements('requirements.txt')

def read_version():
    # Define the path to your __init__.py file where __version__ is set.
    here = os.path.abspath(os.path.dirname(__file__))
    init_path = os.path.join(here, '__init__.py')
    with open(init_path, 'r', encoding='utf-8') as f:
        init_contents = f.read()

    version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", init_contents, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string in __init__.py")


setup(
    name='djautomation',                 # Package name
    version=read_version(),               # Initial version in alpha
    description='A CLI for DJ automation workflows.',  # Short description
    long_description=open('README.md').read(),         # Detailed description from README.md
    long_description_content_type='text/markdown',     # Description format
    author='Katazui',                    # Author name
    author_email='FootLong@Duck.com',    # Author email
    url='https://github.com/Katazui/DJAutomation',  # GitHub repository link
    packages=find_packages(),            # Auto-discover packages in your project
    include_package_data=True,           # Include files specified in MANIFEST.in
    install_requires=install_requires,   # Install dependencies dynamically
    entry_points={                       # CLI script mapping
        'console_scripts': [
            'djcli=cli.main:main',       # CLI command to entry point
        ],
    },
    classifiers=[                        # PyPI metadata
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',             # Minimum Python version required
    tests_require=[
        'pytest',                        # Testing dependencies
    ],
    project_urls={                       # Additional useful links
        'Source': 'https://github.com/Katazui/DJAutomation',
        'Tracker': 'https://github.com/Katazui/DJAutomation/issues',
    },
)