import setuptools
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session="main")
reqs = [str(ir.req) for ir in install_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-locality-system",
    version="0.0.3",
    author="Samuel Michael Squire",
    author_email="sam@samsquire.com",
    description="A library and pattern for low latency applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samsquire/data-locality-system",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=[],
    include_package_data=True,
    install_requires=reqs
)
