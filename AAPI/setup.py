from setuptools import setup, find_packages

setup(
    name="aapi",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        # Add any dependencies your library needs
    ],
    author="AnyActions",
    author_email="your.email@example.com",
    description="A short description of AAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AAPI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)