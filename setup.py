from distutils.core import setup

setup(
    name="leetcode_hard_gym",
    version="0.1.0",
    description="A gym to evaluate superhuman programming agents built on top of OpenAI's [gym]",
    author="Beck Labash, https://github.com/becklabs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={
        "": ["*.txt", "*.rst", "*.md", "*.csv"],
    },
    packages=["leetcode_hard_gym"],
)
