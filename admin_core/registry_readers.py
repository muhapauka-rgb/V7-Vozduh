"""Pure registry parsing helpers for V7 admin surfaces.

This module must stay side-effect free: no runtime paths, no file IO, no shell
commands, and no imports from the admin monolith.
"""


def parse_kv_line(line):
    item = {}
    for part in line.strip().split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        item[key] = value
    return item


def parse_registry_lines(lines):
    items = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        items.append(parse_kv_line(line))
    return items
