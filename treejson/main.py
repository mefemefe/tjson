import sys
from treejson import TreeJson, load_json_input


def main():
    if len(sys.argv) < 2:
        print(sys.argv)
        sys.exit("Usage: treejson <json_string_or_filepath>")

    app = TreeJson(*load_json_input(sys.argv[1]))
    app.run()


if __name__ == "__main__":
    main()
