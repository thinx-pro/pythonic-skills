"""Behavior the refactor must keep. Run with: python -m pytest -q"""

import json

import pytest

import inventory


@pytest.fixture(autouse=True)
def fresh_state(tmp_path, monkeypatch):
    inventory.ITEMS.clear()
    monkeypatch.setattr(inventory, "DATA_DIR", str(tmp_path))
    yield tmp_path
    inventory.ITEMS.clear()


def test_add_accumulates_quantity():
    inventory.add("apple", 3, price=2.0)
    inventory.add("apple", 2, price=2.0)
    assert inventory.ITEMS["apple"]["qty"] == 5


def test_value_is_qty_times_price():
    inventory.add("pear", 4, price=1.5)
    assert inventory.value("pear") == 6.0


def test_load_reads_json_from_data_dir(fresh_state):
    (fresh_state / "stock.json").write_text(
        json.dumps({"fig": {"qty": 7, "price": 3.0}}), encoding="utf-8"
    )
    items = inventory.load("stock.json")
    assert items["fig"]["qty"] == 7
    assert inventory.value("fig") == 21.0


def test_report_skips_empty_unless_asked():
    inventory.add("kiwi", 0, price=1.0)
    inventory.add("plum", 2, price=0.5)
    assert inventory.report(inventory.ITEMS, include_empty=False) == "plum: 2 @ 0.5"
    shown = inventory.report(inventory.ITEMS, include_empty=True).splitlines()
    assert sorted(shown) == ["kiwi: 0 @ 1.0", "plum: 2 @ 0.5"]


def test_save_round_trips(fresh_state):
    inventory.add("lime", 1, price=0.25)
    inventory.save("out.json")
    saved = json.loads((fresh_state / "out.json").read_text(encoding="utf-8"))
    assert saved["lime"]["qty"] == 1
