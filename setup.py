from distutils.core import setup

with open("./prompt_to_code/version.py") as f:
    VERSION = f.read().split("=")[1].strip().strip('"')

setup(
    name="leetcode_hard_gym",
    version=VERSION,
    description="A gym to evaluate superhuman programming agents built on top of OpenAI's [gym]",
    author="Beck Labash, https://github.com/becklabs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={
        "": ["*.txt", "*.rst", "*.md", "*.csv"],
    },
    packages=["leetcode_hard_gym"]
)
