import json
import os
import re
import sys

GLOBAL = {
    "NO_LOG": False
}

def log(message):
    if not GLOBAL["NO_LOG"]:
        print(message)

def process_file(filename):
    if not ".js" in filename:
        return
    lines = []
    with open(filename, "r") as file:
        lines = file.readlines()

    processed = False
    for i, line in enumerate(lines):
        if re.match(r"import", line) == None:
            continue
        if re.search(r"\.js", line):
            continue
        module_pattern = r"\"[\./\w]+\""
        module_name_re = re.search(module_pattern, line)
        module_name_str = module_name_re.group(0)
        module_name_ext = module_name_str[:-1] + ".js\""
        line_processed = line[:module_name_re.span()[0]] + module_name_ext + line[module_name_re.span()[1]:]
        lines[i] = line_processed
        processed = True
    if processed:
        with open(filename, "w") as file:
            file.writelines(lines)
            return True
    return False

def process_folder(foldername):
    for name in os.listdir(foldername):
        path = f"{foldername}/{name}"
        if os.path.isfile(path):
            log(f"[TSMFIX] Checking file \"{name}\"")
            if process_file(path):
                log(f"[TSMFIX] Successfully processed file \"{name}\"")
        elif os.path.isdir(path):
            process_folder(path)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "nolog":
            GLOBAL["NO_LOG"] = True
    if not os.path.exists("./tsconfig.json"):
        log("[TSMFIX] No tsconfig.json found in current working directory")
        return
    tsconfig = {}
    with open("./tsconfig.json", "r") as file:
        tsconfig = json.loads(file.read())
    js_folder = "./" + tsconfig["compilerOptions"]["outDir"]
    process_folder(js_folder)
    

if __name__ == "__main__":
    main()