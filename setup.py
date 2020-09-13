import setuptools
import os

if os.path.exists("README.md"):
    with open("README.md", "r") as f:
        long_description = f.read()
else:
    long_description = ""


setuptools.setup(
    name="mycicd",
    version=os.environ.get("TAG", "0.0.0"),
    author="Hank Doupe",
    author_email="henrymdoupe@gmail.com",
    description=(
        "A simple ci/cd tool. It's not secure for untrusted code but at least it's yours."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hdoupe/mycicd",
    packages=setuptools.find_packages(),
    install_requires=["pyyaml"],
    include_package_data=True,
    entry_points={"console_scripts": ["mycicd=mycicd:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
