import setuptools

setuptools.setup(
    name="OctoPrint-HandCode",
    version="1.0.0",
    description="An OctoPrint plugin to generate handwriting GCode using HandCode.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    entry_points={
        "octoprint.plugin": [
            "handcode = octoprint_handcode"
        ]
    }
)
