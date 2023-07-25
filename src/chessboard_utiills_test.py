import pytest
from collections import deque
from chessboard_utills import E, W, B, translate_fe_notation, one_hot_wbe, translate_fe_to_int_notation


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
    res = translate_fe_notation(test_row)

    assert len(res) == len(expected_res)
    for popped_element, expected_element in zip(res, expected_res):
        assert popped_element == expected_element

@pytest.mark.parametrize(
        "fe_notation, expected_res",
        [
            (
                "1B1K4-2b5-8-8-R3R2P-5k2-N3R1r1-1r2RR2",
                [
                    [E, W, E, W, E, E, E, E],
                    [E, E, B, E, E, E, E, E],
                    [E] * 8,
                    [E] * 8,
                    [W, E, E, E, W, E, E, W],
                    [E, E, E, E, E, B, E, E],
                    [W, E, E, E, W, E, B, E],
                    [E, B, E, E, W, W, E, E],
                ]
            ),
            ("8-8-8-8-8-8-8-8", [[E] * 8] * 8),
            ("NNNNNNNN-NNNNNNNN-NNNNNNNN-NNNNNNNN-NNNNNNNN-NNNNNNNN-NNNNNNNN-NNNNNNNN", [[W] * 8] * 8),
            ("rrrrrrrr-rrrrrrrr-rrrrrrrr-rrrrrrrr-rrrrrrrr-rrrrrrrr-rrrrrrrr-rrrrrrrr", [[B] * 8] * 8),
            (
                "8-rrrrrrrr-NNNNNNNN-8-rrrrrrrr-NNNNNNNN-8-rrrrrrrr",
                [
                    [E] * 8,
                    [B] * 8,
                    [W] * 8,
                    [E] * 8,
                    [B] * 8,
                    [W] * 8,
                    [E] * 8,
                    [B] * 8,
                ]
            ),
        ],
        ids=["full", "empty", "white", "black", "mixed_sequences"],
)
def test_entire_fe(fe_notation, expected_res):
    res = translate_fe_notation(fe_notation=fe_notation)

    expected_res = ["".join(row) for row in expected_res]
    expected_res = "-".join(expected_res)
    assert expected_res == res


def test_fe_to_WBE():
    fe_notation = "1B1K4-2b5-8-8-R3R2P-5k2-N3R1r1-1r2RR2"
    expected_res = "EWEWEEEE-EEBEEEEE-EEEEEEEE-EEEEEEEE-WEEEWEEW-EEEEEBEE-WEEEWEBE-EBEEWWEE"

    res = translate_fe_notation(fe_notation=fe_notation)
    assert expected_res == res


def test_WBE_to_ints():
    def change_2_to_minus1(el):
        el = int(el)
        if el == 2:
            return -1
        return el
    WBE_notation = "EWEWEEEE-EEBEEEEE-EEEEEEEE-EEEEEEEE-WEEEWEEW-EEEEEBEE-WEEEWEBE-EBEEWWEE"
    expected_res = "01010000-00200000-00000000-00000000-10001001-00000200-10001020-02001100".replace(
        "-", "")
    expected_res = list(expected_res)
    expected_res = list(map(change_2_to_minus1, expected_res))
    print(expected_res)
    res = translate_fe_to_int_notation(WBE_notation=WBE_notation)
    assert expected_res == res


@pytest.mark.parametrize('int_notation, expected_res', [
    ([1, 0, -1], ([1, 0, 0], [0, 1, 0], [0, 0, 1])),
    ([0] * 64, ([0] * 64, [1] * 64, [0] * 64)),
    ([1] * 64, ([1] * 64, [0] * 64, [0] * 64)),
    ([-1] * 64, ([0] * 64, [0] * 64, [1] * 64)),
    ([1, 0, 1, -1, 0, 1], ([1, 0, 1, 0, 0, 1], [0, 1, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0]))
])
def test_one_hot_wbe(int_notation, expected_res):
    res = one_hot_wbe(int_notation=int_notation)
    assert res == expected_res
