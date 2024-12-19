from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()


def parse_requirements(file_path):
    with open(file_path, 'r') as file:
        return [
            line.strip() for line in file
            if line.strip() and not line.startswith('#')
        ]


setup(
    name="mxdownloader",
    version="0.2",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        "console_scripts": [
            "mdx = mxdownloader:main",
        ],
    },
    long_description=description,
    long_description_content_type='text/markdown',
)
