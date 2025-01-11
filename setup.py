from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
def parse_requirements(filename):
    """
    Load dependencies from a requirements.txt file.
    """
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Dependencies from requirements.txt
install_requires = parse_requirements('requirements.txt')

setup(
    name='djautomation',                 # Package name
    version='1.0.0',                     # Version number
    description='A CLI for DJ automation workflows.',
    long_description=open('README.md').read(),  # Project description
    long_description_content_type='text/markdown',
    author='Katazui',
    author_email='FootLong@Duck.com',
    url='https://github.com/Katazui/DJAutomation',  # Replace with your repo
    packages=find_packages(),            # Automatically find packages in your project
    include_package_data=True,           # Include non-code files specified in MANIFEST.in
    install_requires=install_requires,   # Load dependencies dynamically
    entry_points={
        'console_scripts': [
            'djcli=cli.main:main',        # Maps `djcli` command to the `main` function
        ],
    },
    classifiers=[                        # Metadata
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',             # Minimum Python version
    tests_require=[
        'pytest',                        # Dependencies for testing
    ],
)