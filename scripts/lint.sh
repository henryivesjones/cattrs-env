#!/bin/bash
# Exit on non-zero returns from commands.
set -e

# Global Variables
RED="\e[31m"
GREEN="\e[32m"
DEFAULT="\e[0m"

# Flag Variables
check_flag=0
verbose_flag=1
fix_flag=0

# CLI Documentation
print_usage() {
    printf "A general workflow before a commit would be to run './lint.sh -f'\n"
    printf "To check if your changes will pass CI/CD checks run './lint.sh -c'\n"
    printf "Usage: ./lint.sh [-c] [-q] [-f]\n[-c] flag is used to test.\n"
    printf "[-q] flag will make the script quiet.\n"
    printf "[-f] flag will try to fix linting errors. (Cannot be used in combination with [-c]\n"
}

# CLI Flag Parser
while getopts 'cqfh' flag; do
    case "${flag}" in
    c) check_flag=1 ;;
    q) verbose_flag=0 ;;
    f) fix_flag=1 ;;
    h) print_usage && exit 0 ;;
    *)
        print_usage
        exit 1
        ;;
    esac
done

##### SCRIPT ######

# Navigate to firehose root directory
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ..

# Set up environment, activate/create venv and install dev requirements
printf "Setting up environment...\n"
python3 -m venv .lint-venv
source .lint-venv/bin/activate

pip3 install -r lint-requirements.txt >>/dev/null 2>/dev/null

# Run checks if check flag is provided. Exit after checks.
if [[ $check_flag -eq 1 ]]; then
    printf "Running checks...\n"
    if [[ $verbose_flag -eq 1 ]]; then
        ruff check .
        black . --check
    else
        ruff check . -s || (printf "${RED}FAILURE: Failed ruff checks.${DEFAULT}\n" && exit 1)

        black . --check -q || (printf "${RED}FAILURE: Would reformat files.${DEFAULT}\n" && exit 1)
    fi
    printf "${GREEN}SUCCESS: All checks passed.${DEFAULT}\n"
    exit 0
fi

# If fix flag provided, then run ruff --fix.
# If ruff encounters errors that it cannot fix, then the formatting step will not run.
# Run black over codebase, formatting code.
if [[ $verbose_flag -eq 1 ]]; then
    if [[ $fix_flag -eq 1 ]]; then
        printf "Fixing linting errors...\n"
        ruff --fix .
    fi
    printf "Formatting Code...\n"
    black .
else
    if [[ $fix_flag -eq 1 ]]; then
        printf "Fixing linting errors...\n"
        ruff --fix . -s || (printf "${RED}FAILURE: Failed ruff checks.${DEFAULT}\n" && exit 1)
        black . -q
    fi
    printf "Formatting Code...\n"
    black . -q
fi

# If the script hasn't already exited then we are successfull.
# Does not indicate that -c will pass, unless -f flag was provided.
printf "${GREEN}SUCCESS: Formatting complete.\n${DEFAULT}"
