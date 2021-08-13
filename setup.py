import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysteamsignin",
    version="1.0.0",
    author="TeddiO",
    author_email="",
    description="OpenID sign in for steam",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeddiO/pySteamSignIn",
    project_urls={
        "Bug Tracker": "https://github.com/TeddiO/pySteamSignIn/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=('samples')),
    python_requires=">=3.6"
)