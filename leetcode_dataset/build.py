import os
import logging
import argparse
from lib.fetch_dataset import fetch_dataset
from lib.utils.utils import get_api_instance
from lib.clean_dataset import remove_class_dependent, remove_void, remove_class_impls, remove_examples
from lib.format_dataset import format_problems, to_jsonl

parser = argparse.ArgumentParser(description="Configuration for building uncontaminated Leetcode Hard dataset")
parser.add_argument('--langs', nargs='+', default=['python3'], help="List of languages. Possible options are: rust, python3")
parser.add_argument('--log_level', type=str, default='INFO', help="Logging level. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL.")
parser.add_argument('--output_dir', type=str, default="./build", help="Directory to save the built dataset.")
parser.add_argument('--extract_test_cases', action='store_true', help="If set, test cases will be extracted from problem descriptions using GPT.")
parser.add_argument('--remove_examples', action='store_true', help="If set, examples will be removed. Cannot be used with --extract_test_cases.")

args = parser.parse_args()

langs = args.langs
log_level = getattr(logging, args.log_level.upper())
output_dir = args.output_dir
extract_test_cases = args.extract_test_cases
remove_examples_ = args.remove_examples

try:
    os.environ["LEETCODE_SESSION"]
except:
    print("Environment variable LEETCODE_SESSION is not set. Please refer to README")
    exit(1)

if extract_test_cases:
    try:
        os.environ["OPENAI_API_KEY"]
        import openai
        import langchain
    except:
        print("Extra dependencies and setup are required for test case extraction. Please refer to README")
        exit(1)
    if remove_examples_:
        print("Cannot use --remove_examples with --extract_test_cases")
        exit(1)


logging.basicConfig(level=log_level)
os.makedirs(output_dir, exist_ok=True)

api_instance = get_api_instance()
dataset = fetch_dataset(api_instance)

filtered_dataset = \
    remove_class_impls(
    remove_void(
    remove_class_dependent(dataset)))

if remove_examples_:
    filtered_dataset = remove_examples(filtered_dataset)

logging.info(f"Filtered out {len(dataset) - len(filtered_dataset)} problem(s)")

for lang in langs:
    logging.info(f"Formatting dataset for {lang}")
    formatted_dataset = format_problems(filtered_dataset, lang)
    if extract_test_cases:
        from lib.add_test_cases import extract_test_cases
        formatted_dataset = extract_test_cases(formatted_dataset, lang)
    to_jsonl(formatted_dataset, os.path.join(output_dir, f'leetcode-hard-uncontaminated-{lang}.jsonl'))
