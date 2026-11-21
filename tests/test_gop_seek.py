import pytest
import math
from media import gop_seek as mod

CASES = [
    ("keyframe", 'm.nearest_keyframe(7, [0, 5, 10]) == 5'),
    ("decode", 'm.decode_until(7, 5) == 2'),
    ("bframe", 'm.bframe_pts(3, 2) == 5'),
    ("edit", 'm.edit_offset(10, 2) == 8'),
    ("vfr", 'm.vfr_time([1, 2, 3], 2) == 3'),
    ("sync", 'm.sync_audio(5, 0.5) == approx(5.5)'),
    ("params", 'm.reset_params(1, 2) == 2'),
    ("preroll", 'm.preroll(10) == 20'),
    ("queue", 'm.clear_queue(5) == 0'),
    ("index", 'm.lookup_index([0, 2, 4], 1) == 0'),
    ("gop", 'm.gop_start(7, 5) == 5'),
    ("byte", 'm.byte_to_time(1000, 500) == approx(2.0)'),
    ("valid", 'm.valid_keyframe(0) is True'),
    ("key", 'm.seek_key(3, 2) == "3:2"'),
    ("dur", 'm.frame_duration(25) == approx(0.04)')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
