#!/usr/bin/env python3
from sys import argv, stdin
def tangle(out_paths):
    files = {}
    try:

        for e in (e for i, e in enumerate(stdin.read().split("```")) if i % 2 == 1):
            lines = e.split("\n")
            header = lines[0].split()
            try:
                lang = header[0]
            except IndexError:
                continue
            try:
                name = header[1]
            except IndexError:
                name = lang
            path = out_paths[name]
            while True:
                try:
                    files[path].write("\n".join(lines[1:]))
                    break
                except KeyError:
                    files[path] = open(path, "w")

    finally:
        for p, f in files.items():
            f.close()


tangle(dict(name_path.split(":") for name_path in argv[1:]))
# implied stream name = lang name for each lang
