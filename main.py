import json
import sys
import zipfile

def print_output(field):
    print(field["title"], ':\n', field["value"]["concealed"], '\n')


def extract_secrets(pux_file):
    with zipfile.ZipFile(pux_file, 'r') as z:
        with z.open("export.data") as f:
            data = json.load(f)
            for account in data["accounts"]:
                for vault in account["vaults"]:
                    if account["vaults"] != "Archive":
                        for item in vault["items"]:
                            if len(item["details"]["sections"]):
                                item_name = item["overview"]["title"]
                                for section in item["details"]["sections"]:
                                    if section["title"] == "Security Questions":
                                        print('**** ', item_name, ' ****')
                                        for field in section["fields"]:
                                            print_output(field)
                                    if section["title"] == "":
                                        for field in section["fields"]:
                                            if field["title"] == "Recovery Key":
                                                print('**** ', item_name, ' ****')
                                                print_output(field)


def main():
    try:
        pux_file = sys.argv[1]
        extract_secrets(pux_file)
    except Exception as e:
        print("\nHINT: Command should be invoked as: python main.py [1PUX_FILE]")
        print("\n", e)

if __name__ == "__main__":
    main()