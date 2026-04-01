# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pgpro_pytest_html_merger import __main__ as prog

# //////////////////////////////////////////////////////////////////////////////


class TestSet006__pytest_report_env_prop_id:
    @dataclasses.dataclass
    class tagData006:
        sign: str
        p1: int
        p2: typing.Optional[int]
        expected_repr: str

    # --------------------------------------------------------------------
    # 1. Test basic creation and properties
    sm_Data006Ok: typing.List[tagData006] = [
        tagData006("full_id", 100, 5, "PytestReportEnvPropID(part1=100, part2=5)"),
        tagData006(
            "partial_id", 200, None, "PytestReportEnvPropID(part1=200, part2=None)"
        ),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data006Ok, ids=[x.sign for x in sm_Data006Ok])
    def data006ok(self, request: pytest.FixtureRequest) -> tagData006:
        return request.param

    # --------------------------------------------------------------------
    def test_006_properties_and_repr(self, data006ok: tagData006):
        # Create object
        obj = prog.PytestReportEnvPropID(data006ok.p1, data006ok.p2)

        # Check properties
        assert type(obj.part1) is int
        assert obj.part1 == data006ok.p1

        if data006ok.p2 is not None:
            assert type(obj.part2) is int
        else:
            assert obj.part2 is None
        assert obj.part2 == data006ok.p2

        # Check string representation (important for debugging)
        assert repr(obj) == data006ok.expected_repr
        return

    # --------------------------------------------------------------------
    # 2. Test Equality (__eq__)
    def test_006_equality(self):
        id1 = prog.PytestReportEnvPropID(1, 10)
        id2 = prog.PytestReportEnvPropID(1, 10)
        id3 = prog.PytestReportEnvPropID(1, None)
        id4 = prog.PytestReportEnvPropID(2, 10)

        assert id1 == id2
        assert id1 != id3
        assert id1 != id4
        assert id1 != "not_an_id_object"
        return

    # --------------------------------------------------------------------
    # 3. Test Sorting (__lt__) - This is the "concrete" part
    def test_006_sorting(self):
        # Unsorted list with various combinations
        p1 = prog.PytestReportEnvPropID(10, 5)
        p2 = prog.PytestReportEnvPropID(5, 100)
        p3 = prog.PytestReportEnvPropID(10, None)
        p4 = prog.PytestReportEnvPropID(5, 10)
        p5 = prog.PytestReportEnvPropID(5, None)

        unsorted = [
            p1,
            p2,
            p3,
            p4,
            p5,
        ]

        # Expected order:
        # 1. part1=5, part2=None
        # 2. part1=5, part2=10
        # 3. part1=5, part2=100
        # 4. part1=10, part2=None
        # 5. part1=10, part2=5
        sorted_list = sorted(unsorted)

        assert sorted_list[0] is p5
        assert sorted_list[1] is p4
        assert sorted_list[2] is p2
        assert sorted_list[3] is p3
        assert sorted_list[4] is p1

        assert sorted_list[0].part1 == 5 and sorted_list[0].part2 is None
        assert sorted_list[1].part1 == 5 and sorted_list[1].part2 == 10
        assert sorted_list[2].part1 == 5 and sorted_list[2].part2 == 100
        assert sorted_list[3].part1 == 10 and sorted_list[3].part2 is None
        assert sorted_list[4].part1 == 10 and sorted_list[4].part2 == 5
        return


# //////////////////////////////////////////////////////////////////////////////
