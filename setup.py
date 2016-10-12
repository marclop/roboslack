import io
from setuptools import setup
from roboslack.version import version


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read("README.md")
install_requires = [
    "requests==2.11.1",
    "slacksocket==0.7"
]

install_dev_requires = [
    "pytest==3.0.3",
    "py==1.4.31"
]

setup(
    name="roboslack",
    version=version,
    packages=["roboslack"],
    url="http://github.com/marclop/roboslack",
    author="Marc Lopez",
    author_email="marc5.12@outlook.com",
    tests_require=install_dev_requires,
    install_requires=install_requires,
    description="Simple bot Framework using RTM Websocket API",
    include_package_data=True,
    keywords="slack bot slackbot robot",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License ",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
    ],
)
