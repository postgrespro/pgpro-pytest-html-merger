# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pgpro_pytest_html_merger import __main__ as prog

from .helpers import Helper

# //////////////////////////////////////////////////////////////////////////////


class TestSet004__pytest_report_env_prop_list_create:
    @dataclasses.dataclass
    class tagData004:
        sign: str
        report_id: int
        env_dict: typing.Dict[str, typing.Any]
        expected_list: prog.PytestReportEnvPropList

    # --------------------------------------------------------------------
    # Helper to build the expected structure in a fluent way
    @staticmethod
    def build_list() -> prog.PytestReportEnvPropList:
        return prog.PytestReportEnvPropList()

    # --------------------------------------------------------------------
    sm_Data004Ok: typing.List[tagData004] = [
        # 0. None
        tagData004(
            sign="none value",
            report_id=11,
            env_dict={"Branch": None},
            expected_list=prog.PytestReportEnvPropList().helper_add(
                "Branch", prog.PytestReportEnvPropID(11, None), None
            ),
        ),
        # 1. Simple flat dictionary
        tagData004(
            sign="simple_flat",
            report_id=10,
            env_dict={"OS": "Linux"},
            expected_list=prog.PytestReportEnvPropList().helper_add(
                "OS", prog.PytestReportEnvPropID(10, None), "Linux"
            ),
        ),
        # 2. Explicit ID override
        tagData004(
            sign="explicit_id",
            report_id=10,
            env_dict={"Python {99}": "3.8"},
            expected_list=prog.PytestReportEnvPropList().helper_add(
                "Python", prog.PytestReportEnvPropID(10, 99), "3.8"
            ),
        ),
        # 3. Deep recursion check
        tagData004(
            sign="recursive_nesting",
            report_id=1,
            env_dict={
                "Database": {"Server": "Postgres", "Port {123}": "5432"},
                "User": {
                    "ID": "Bob",
                    "PSWD": "secret",
                },
            },
            expected_list=prog.PytestReportEnvPropList()
            .helper_add(
                "Database",
                prog.PytestReportEnvPropID(1, None),
                prog.PytestReportEnvPropList()
                .helper_add("Server", prog.PytestReportEnvPropID(1, None), "Postgres")
                .helper_add("Port", prog.PytestReportEnvPropID(1, 123), "5432"),
            )
            .helper_add(
                "User",
                prog.PytestReportEnvPropID(1, None),
                prog.PytestReportEnvPropList()
                .helper_add("ID", prog.PytestReportEnvPropID(1, None), "Bob")
                .helper_add("PSWD", prog.PytestReportEnvPropID(1, None), "secret"),
            ),
        ),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data004Ok, ids=[x.sign for x in sm_Data004Ok])
    def data004ok(self, request: pytest.FixtureRequest) -> tagData004:
        return request.param

    # --------------------------------------------------------------------
    def test_004_create_deep_check(self, data004ok: tagData004):
        # 1. Type validation
        assert type(data004ok) is __class__.tagData004

        # 2. Execution
        actual_list = prog.PytestReportEnvPropList.create(
            data004ok.report_id, data004ok.env_dict
        )

        # 3. Full recursive comparison
        Helper.compare_prop_lists(actual_list, data004ok.expected_list)


# //////////////////////////////////////////////////////////////////////////////
