import pytest
from collections import deque
from chess_utils import E, W, B, _translate_fe_row, translate_fe


@pytest.mark.parametrize(
    "test_row, expected_res",
    [
        ("8", [E] * 8),
        ("1B1K4", [E, W, E, W, E, E, E, E]),
        ("2b5", [E, E, B, E, E, E, E, E]),
        ("R3R2P", [W, E, E, E, W, E, E, W]),
        ("5k2", [E, E, E, E, E, B, E, E]),
        ("N3R1r1", [W, E, E, E, W, E, B, E]),
        ("1r2RR2", [E, B, E, E, W, W, E, E]),
    ],
)
def test_row_8_digits(test_row, expected_res):
    res = _translate_fe_row(test_row)

    assert len(res) == len(expected_res)
    for popped_element, expected_element in zip(res, expected_res):
        assert popped_element == expected_element


def test_entire_fe():
    fe_notation = "1B1K4-2b5-8-8-R3R2P-5k2-N3R1r1-1r2RR2"
    expected_res = [
        deque([E, W, E, W, E, E, E, E]),
        deque([E, E, B, E, E, E, E, E]),
        deque([E] * 8),
        deque([E] * 8),
        deque([W, E, E, E, W, E, E, W]),
        deque([E, E, E, E, E, B, E, E]),
        deque([W, E, E, E, W, E, B, E]),
        deque([E, B, E, E, W, W, E, E]),
    ]
    res = translate_fe(fe_notation=fe_notation)
    assert res == expected_res
