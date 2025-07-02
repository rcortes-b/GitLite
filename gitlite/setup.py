from setuptools import setup, find_packages

setup(
    name="gitlite",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # add any deps if needed
    entry_points={
        "console_scripts": [
            "gitlite=gitlite.main:main",  # points to main() function
        ],
    },
    author="Your Name",
    description="A lightweight Git-like tool written in Python.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
)
