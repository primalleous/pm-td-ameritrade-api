from setuptools import setup
from setuptools import find_namespace_packages

# load the README file.
with open(file="README.md", mode="r") as fh:
    long_description = fh.read()

setup(
    name="pm-td-ameritrade-api",
    author="Zach Fortier",
    author_email="primalmachinaz@gmail.com",
    version="0.1.3",
    description="A python client lirbary for the TD Ameritrade API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/primalmachina/pm-td-ameritrade-api",
    install_requires=[
        "aiofiles>=0.7.0",
        "pydantic>=1.10.2",
        "rich>=13.2.0",
        "websockets>=10.4",
        "pyhumps>=3.7.1",
        "colorlog>=6.7.0",
        "selenium>=4.7.2",
        "requests>=2.28.1",
    ],
    keywords="finance, td ameritrade, api",
    packages=find_namespace_packages(
        include=["pm_td_ameritrade_api.*"], exclude=["config*"]
    ),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",
)
