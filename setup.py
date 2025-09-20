import setuptools

def find_packages():
    return setuptools.find_packages(exclude=("test*",))

def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()

setuptools.setup(
    name="OctoPrint-HandCode",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/YourUsername/OctoPrint-HandCode",
    description="Integrates the HandCode handwriting GCode generator with OctoPrint.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="AGPLv3",
    packages=find_packages(),
    install_requires=read_requirements(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "octoprint.plugin": [
            "handcode = octoprint_handcode"
        ]
    },
    python_requires=">=3.7",
)

