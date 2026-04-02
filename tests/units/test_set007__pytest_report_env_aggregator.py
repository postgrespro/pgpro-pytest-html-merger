# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pgpro_pytest_html_merger import __main__ as prog

from .helpers import Helper

# //////////////////////////////////////////////////////////////////////////////
# Static verification helper for complex cases


# //////////////////////////////////////////////////////////////////////////////


class TestSet007__pytest_report_env_aggregator:
    @dataclasses.dataclass
    class tagData007:
        sign: str
        input_dicts: typing.List[typing.Dict[str, typing.Any]]
        expected_list: prog.PytestReportEnvPropList

    # --------------------------------------------------------------------
    # Helper to create PropList from dict for tests
    @staticmethod
    def create_list(
        report_id: int, data: typing.Dict[str, typing.Any]
    ) -> prog.PytestReportEnvPropList:
        return prog.PytestReportEnvPropList.create(report_id, data)

    # --------------------------------------------------------------------
    sm_Data007Ok: typing.List[tagData007] = [
        # 1. Deduplication: Same key, same value -> One item
        tagData007(
            sign="deduplication_simple",
            input_dicts=[{"OS": "Linux"}, {"OS": "Linux"}],
            expected_list=prog.PytestReportEnvPropList().helper_add(
                "OS",
                prog.PytestReportEnvPropID(1, None),
                "Linux",
            ),
        ),
        # 2. Duplication: Same key, different values -> Two items (for future ID tagging)
        tagData007(
            sign="keep_different_values",
            input_dicts=[{"Python": "3.8"}, {"Python": "3.9"}],
            expected_list=prog.PytestReportEnvPropList()
            .helper_add(
                "Python",
                prog.PytestReportEnvPropID(1, None),
                "3.8",
            )
            .helper_add(
                "Python",
                prog.PytestReportEnvPropID(2, None),
                "3.9",
            ),
        ),
        # 3. Recursive Merge: Nested dictionaries should merge into one PropList
        tagData007(
            sign="recursive_merge",
            input_dicts=[{"Libs": {"pytest": "7.0"}}, {"Libs": {"requests": "2.0"}}],
            expected_list=prog.PytestReportEnvPropList().helper_add(
                "Libs",
                prog.PytestReportEnvPropID(1, None),
                prog.PytestReportEnvPropList()
                .helper_add(
                    "pytest",
                    prog.PytestReportEnvPropID(1, None),
                    "7.0",
                )
                .helper_add(
                    "requests",
                    prog.PytestReportEnvPropID(2, None),
                    "2.0",
                ),
            ),
        ),
        # 4. Mixed Types: dict vs str with same name -> Should keep both
        tagData007(
            sign="mixed_types_same_name",
            input_dicts=[{"Env": "Prod"}, {"Env": {"Level": "1"}}],
            expected_list=prog.PytestReportEnvPropList()
            .helper_add("Env", prog.PytestReportEnvPropID(1, None), "Prod")
            .helper_add(
                "Env",
                prog.PytestReportEnvPropID(2, None),
                prog.PytestReportEnvPropList().helper_add(
                    "Level",
                    prog.PytestReportEnvPropID(2, None),
                    "1",
                ),
            ),
        ),
        # None + None
        tagData007(
            sign="none_and_none",
            input_dicts=[{"Prop": None}, {"Prop": None}],
            expected_list=prog.PytestReportEnvPropList().helper_add(
                "Prop", prog.PytestReportEnvPropID(1, None), None
            ),
        ),
        # None + None + ""
        tagData007(
            sign="none_and_none_and_empty",
            input_dicts=[{"Prop": None}, {"Prop": None}, {"Prop": ""}],
            expected_list=prog.PytestReportEnvPropList()
            .helper_add("Prop", prog.PytestReportEnvPropID(1, None), None)
            .helper_add("Prop", prog.PytestReportEnvPropID(3, None), ""),
        ),
        # None + dict
        tagData007(
            sign="none_and_dict",
            input_dicts=[{"Prop": None}, {"Prop": {"Level": "1"}}],
            expected_list=prog.PytestReportEnvPropList()
            .helper_add("Prop", prog.PytestReportEnvPropID(1, None), None)
            .helper_add(
                "Prop",
                prog.PytestReportEnvPropID(2, None),
                prog.PytestReportEnvPropList().helper_add(
                    "Level",
                    prog.PytestReportEnvPropID(2, None),
                    "1",
                ),
            ),
        ),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data007Ok, ids=[x.sign for x in sm_Data007Ok])
    def data007ok(self, request: pytest.FixtureRequest) -> tagData007:
        return request.param

    # --------------------------------------------------------------------
    def test_007_aggregator_logic(self, data007ok: tagData007):
        # 1. Validation
        assert type(data007ok) is __class__.tagData007

        aggregator = prog.PytestReportEnvAggregator()

        # 2. Add multiple reports to aggregator
        report_id = 0
        for d in data007ok.input_dicts:
            report_id += 1
            prop_list = self.create_list(report_id, d)
            aggregator.add(prop_list)

        # 3. Result check
        result = aggregator._result
        assert type(result) is prog.PytestReportEnvPropList
        Helper.compare_prop_lists(result, data007ok.expected_list)
        return


# //////////////////////////////////////////////////////////////////////////////
