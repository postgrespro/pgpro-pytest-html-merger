# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pgpro_pytest_html_merger import __main__ as prog

# //////////////////////////////////////////////////////////////////////////////


class TestSet008__pytest_report_env_prop_list_build_dict:
    @dataclasses.dataclass
    class tagData008:
        sign: str
        input_list: prog.PytestReportEnvPropList
        expected_dict: typing.Dict[str, typing.Any]

    # Helper to build IDs and Props quickly for test data
    def _id(p1: int, p2: typing.Optional[int] = None) -> prog.PytestReportEnvPropID:
        return prog.PytestReportEnvPropID(p1, p2)

    sm_Data008Ok: typing.List[tagData008] = [
        # 1. Using your new simplified helper_add(name, id, value)
        tagData008(
            sign="unique_names",
            input_list=prog.PytestReportEnvPropList()
            .helper_add("OS", _id(1), "Linux")
            .helper_add("Arch", _id(1), "x86_64"),
            expected_dict={"OS": "Linux", "Arch": "x86_64"},
        ),
        # 2. Duplicate names check with stable sorting
        tagData008(
            sign="duplicate_names_sorting",
            input_list=prog.PytestReportEnvPropList()
            # Adding ID(2) before ID(1) to test sorting logic
            .helper_add("Python", _id(2), "3.9").helper_add("Python", _id(1), "3.8"),
            expected_dict={"Python {1}": "3.8", "Python {2}": "3.9"},
        ),
        # 3. Recursive nesting with the new simplified syntax
        tagData008(
            sign="recursive_duplicates",
            input_list=prog.PytestReportEnvPropList()
            .helper_add(
                "Libs",
                _id(1),
                prog.PytestReportEnvPropList().helper_add("pytest", _id(1), "7.0"),
            )
            .helper_add(
                "Libs",
                _id(2),
                prog.PytestReportEnvPropList().helper_add("pytest", _id(1), "8.0"),
            ),
            expected_dict={
                "Libs {1}": {"pytest": "7.0"},
                "Libs {2}": {"pytest": "8.0"},
            },
        ),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data008Ok, ids=[x.sign for x in sm_Data008Ok])
    def data008ok(self, request: pytest.FixtureRequest) -> tagData008:
        return request.param

    # --------------------------------------------------------------------
    def test_008_build_dict_accuracy(self, data008ok: tagData008):
        # 1. Type validation
        assert type(data008ok) is __class__.tagData008

        # 2. Execution
        actual_dict = data008ok.input_list.build_dict()

        # 3. Precise comparison
        # This checks keys, values, and nesting depth
        assert actual_dict == data008ok.expected_dict

        # 4. Extra check for key format if duplicates exist
        # If we have more than one item in input, check if braces are present
        if len(data008ok.input_list.m_items) > 1:
            # If names were the same, braces MUST be there
            all_names = [p.name for p in data008ok.input_list.m_items]
            if len(set(all_names)) < len(all_names):
                for key in actual_dict.keys():
                    if " {" in key:
                        assert key.endswith("}")


# //////////////////////////////////////////////////////////////////////////////
