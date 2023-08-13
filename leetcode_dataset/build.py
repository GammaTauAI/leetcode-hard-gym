import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="A simple build script for Python and Rust.")
    parser.add_argument(
        "--lang",
        choices=["python", "rust"],
        required=True,
        help="The programming language for the build. Choices: 'python' or 'rust'.",
    )

    # Add output directory argument that defaults to os.getcwd()
    parser.add_argument(
        "--output_dir",
        default=os.getcwd(),
        help="The directory to output the build artifacts.",
    )


    # Add an argument called keep_temp that defaults to false
    parser.add_argument(
        "--keep_temp",
        action="store_true",
        help="Keep the temporary build directory.",
    )

    args = parser.parse_args() 

    build_dataset(args)

import leetcode
import leetcode.auth
configuration = leetcode.Configuration()

# From Dev Tools/Application/Cookies/LEETCODE_SESSION
leetcode_session = os.environ["LEETCODE_SESSION"]
csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

def build_dataset(args):
    if args.lang == "python":
        print("Building a Python project...")
        # Add your Python build logic here
    elif args.lang == "rust":
        print("Building a Rust project...")
        # Add your Rust build logic here


if __name__ == "__main__":
    main()
