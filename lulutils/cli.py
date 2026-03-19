import sys
from lulutils.utils import resolve_filepath

COMMANDS = {
    "resolve-filepath": resolve_filepath,
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Usage: lulutils <command> [args]")
        print(f"Commands: {', '.join(COMMANDS)}")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "resolve-filepath":
        if len(args) != 1:
            print("Usage: lulutils resolve-filepath <uri>")
            sys.exit(1)
        print(resolve_filepath(args[0]))
