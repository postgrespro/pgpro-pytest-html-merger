# //////////////////////////////////////////////////////////////////////////////
import pytest
import typing
import dataclasses

from src.pgpro_pytest_html_merger import __main__ as prog

# //////////////////////////////////////////////////////////////////////////////


class TestSet005__pytest_report_env_prop_list_create_errors:
    @dataclasses.dataclass
    class tagData005:
        sign: str
        report_id: int
        invalid_env: typing.Dict[str, typing.Any]
        expected_error_msg: str

    # We use types that are NOT str or dict to trigger the RuntimeError
    sm_Data005Fail: typing.List[tagData005] = [
        # 0. None value (Unsupported)
        tagData005(
            sign="none_value",
            report_id=1,
            invalid_env={"Timeout": None},
            expected_error_msg=prog.ErrMsgGenerator.gen_msg__env_prop_is_none(
                "Timeout",
            ),
        ),
        # 1. Integer value (Unsupported)
        tagData005(
            sign="int_value",
            report_id=1,
            invalid_env={"Timeout": 30},
            expected_error_msg=prog.ErrMsgGenerator.gen_msg__unsupported_env_prop_type(
                "Timeout", "int"
            ),
        ),
        # 2. List value (Unsupported for now)
        tagData005(
            sign="list_value",
            report_id=1,
            invalid_env={"Nodes": ["node1", "node2"]},
            expected_error_msg=prog.ErrMsgGenerator.gen_msg__unsupported_env_prop_type(
                "Nodes", "list"
            ),
        ),
    ]

    # --------------------------------------------------------------------
    @pytest.fixture(params=sm_Data005Fail, ids=[x.sign for x in sm_Data005Fail])
    def data005fail(self, request: pytest.FixtureRequest) -> tagData005:
        return request.param

    # --------------------------------------------------------------------
    def test_005_create_fails(self, data005fail: tagData005):
        assert type(data005fail) is __class__.tagData005

        # Now we expect RuntimeError for all these cases since we replaced asserts
        with pytest.raises(RuntimeError) as excinfo:
            prog.PytestReportEnvPropList.create(
                data005fail.report_id, data005fail.invalid_env
            )

        # Strict message comparison
        assert str(excinfo.value) == data005fail.expected_error_msg
        return


# //////////////////////////////////////////////////////////////////////////////
