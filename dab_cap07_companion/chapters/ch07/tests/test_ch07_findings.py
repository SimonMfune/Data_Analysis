"""Guards the numbers Chapter 7 prints. Run from the repository root: pytest chapters/ch07/tests"""
from pathlib import Path

OUT = Path("chapters/ch07/outputs")
read = lambda name: (OUT / name).read_text()

def test_payday_matches_chapter_4():
    assert "65.0 orders a day; rest of month: 49.9" in read("07_08_payday.txt")

def test_december_peak():
    assert "1.99 times" in read("07_07_monthly.txt")

def test_repeat_rate_rises():
    text = read("07_15_repeat_rate.txt")
    assert "2023Q1   79.10" in text and "2025Q3   86.50" in text

def test_late_delivery():
    text = read("07_16_delivery.txt")
    assert "Overall: 12.5% late" in text and "Lusaka         15756     10.80" in text

def test_rfm_segment_sizes():
    text = read("07_14_rfm_segments.txt")
    for seg, n in [("Champions", 999), ("Lost", 981), ("At risk", 344)]:
        assert any(line.startswith(seg) and f" {n} " in line for line in text.splitlines())
