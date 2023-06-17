from modules.parse.parsewrapper import calc_evaluation
import pytest


@pytest.mark.parametrize("evaluation, result", [("2+2", 4.0),
                                                ("3*(2**2)", 12.0)])
def test_parser(evaluation, result):
    assert calc_evaluation(evaluation) == result
