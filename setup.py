from setuptools import setup, find_packages

def parse_requirements(filename):
    """
    Parse a requirements file to load dependencies.
    Skips empty lines and comments.
    """
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Load dependencies from requirements.txt
install_requires = parse_requirements('requirements.txt')

setup(
    name='djautomation',                 # Package name
    version='1.1.0-alpha',               # Initial version in alpha
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