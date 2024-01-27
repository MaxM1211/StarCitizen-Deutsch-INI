import json
from configparser import ConfigParser

filename_eng = "en/live/global.ini"
filename_ger = "live/global.ini"


def addLine(filename, line):
    with open(filename, encoding="utf_8_sig", mode="r+") as file:
        file_data = file.read()
        file.seek(0, 0)
        file.write(line + ("\n") + file_data)


def removeFirstLine(filename):
    with open(filename, encoding="utf_8_sig", mode="r+") as file:
        lines = file.readlines()
        file.seek(0, 0)
        file.truncate()
        file.writelines(lines[1:])


line = "[DEFAULT]"
file_data = ""

addLine(filename=filename_eng, line=line)
addLine(filename=filename_ger, line=line)

config_eng = ConfigParser(
    allow_no_value=True, comment_prefixes=None, delimiters=("="), interpolation=None
)
config_ger = ConfigParser(
    allow_no_value=True, comment_prefixes=None, delimiters=("="), interpolation=None
)
config_eng.read(filename_eng, "utf_8_sig")
config_eng_section = config_eng["DEFAULT"]

config_ger.read(filename_ger, "utf_8_sig")
config_ger_section = config_ger["DEFAULT"]

not_found_keys = {}

line = 1
for key in config_eng_section.keys():
    value = config_ger_section.get(key)
    if value == None:
        not_found_keys[line] = key
    line += 1

removeFirstLine(filename_eng)
removeFirstLine(filename_ger)

if len(not_found_keys):
    import os
    import uuid

    def set_output(name, value):
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            print(f"{name}={value}", file=fh)

    def set_multiline_output(name, value):
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            delimiter = uuid.uuid1()
            print(f"{name}<<{delimiter}", file=fh)
            print(value, file=fh)
            print(delimiter, file=fh)

    print(json.dumps(not_found_keys, indent=4))
    try:
        set_output("test_report", json.dumps(not_found_keys, indent=4))
        # set_multiline_output("test_report",json.dumps(not_found_keys, indent=4))
    except:
        pass
    exit(1)
