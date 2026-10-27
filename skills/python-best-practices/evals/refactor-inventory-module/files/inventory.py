import os, json
import datetime

# global inventory state
ITEMS = {}
DATA_DIR = "data"
DEBUG = True


def load(path, defaults={}):
    try:
        f = open(os.path.join(DATA_DIR, path))
        raw = json.load(f)
        for name in raw:
            entry = defaults.copy()
            entry.update(raw[name])
            entry["qty"] = eval(str(entry.get("qty", 0)))
            ITEMS[name] = entry
        if DEBUG:
            print("loaded", len(raw), "items")
        return ITEMS
    except:
        return None


def add(name, qty, price=None, tags=[]):
    global ITEMS
    if ITEMS.get(name) == None:
        ITEMS[name] = {"qty": 0, "price": price, "tags": tags}
    ITEMS[name]["qty"] += qty
    tags.append("added")
    ITEMS[name]["updated"] = datetime.datetime.utcnow().isoformat()


def value(name):
    item = ITEMS.get(name, {})
    return item.get("qty", 0) * item.get("price", 0)


def report(items, include_empty):
    lines = []
    for name in set(items):
        item = items[name]
        if item["qty"] == 0 and not include_empty:
            continue
        lines.append(name + ": " + str(item["qty"]) + " @ " + str(item.get("price")))
    return "\n".join(lines)


def save(path):
    f = open(os.path.join(DATA_DIR, path), "w")
    f.write(json.dumps(ITEMS))
    f.close()
