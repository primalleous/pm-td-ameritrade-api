from setuptools import find_namespace_packages, setup

# load the README file.
with open(file="README.md", mode="r") as fh:
    long_description = fh.read()

setup(
    name="pm-td-ameritrade-api",
    author="primaleae",
    author_email="primaleae@gmail.com",
    version="0.9.0",
    description="A python client library for the TD Ameritrade API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/primalmachinai/pm-td-ameritrade-api",
    install_requires=[
        "aiofiles>=23.2.1",
        "pydantic>=2.4.2",
        "rich>=13.6.0",
        "websockets>=11.0.3",
        "colorlog>=6.7.0",
        "selenium>=4.14.0",
        "requests>=2.31.0",
        "webdriver_manager>=4.0.1",
    ],
    keywords="finance, td ameritrade, api",
    packages=find_namespace_packages(
        include=["pm_td_ameritrade_api.*"], exclude=["config*"]
    ),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",
)
