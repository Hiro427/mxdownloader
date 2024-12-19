from setuptools import setup, find_packages


def parse_requirements(file_path):
    with open(file_path, 'r') as file:
        return [
            line.strip() for line in file
            if line.strip() and not line.startswith('#')
        ]


setup(
    name="mxdownloader",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mdx = mxdownloader:main",
        ],
    },
    description="Download Manga using the MangaDex API",
    license="MIT",
    long_description=
    "Visit the project's [GitHub page](https://github.com/Hiro427/mxdownloader) for more info. ![Screenshot from 2024-09-23 16-35-13](https://github.com/user-attachments/assets/043f42e7-6fb9-4634-bdc2-bf1030577f44)",
    long_description_content_type="text/markdown",
    url="https://github.com/Hiro427/mxdownloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author="Jacob Rambarran",
    install_requires=parse_requirements('requirements.txt'),
)
