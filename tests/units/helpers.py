from src.pgpro_pytest_html_merger import __main__ as prog


class Helper:
    @staticmethod
    def compare_prop_lists(
        actual: prog.PytestReportEnvPropList,
        expected: prog.PytestReportEnvPropList,
    ):
        """
        Recursively compares two PytestReportEnvPropList objects.
        """
        assert len(actual.m_items) == len(expected.m_items), "Items count mismatch"

        for a_item, e_item in zip(actual.m_items, expected.m_items):
            assert type(a_item) is prog.PytestReportEnvProp
            assert type(e_item) is prog.PytestReportEnvProp
            assert a_item.name == e_item.name
            assert a_item.id == e_item.id

            if type(e_item.value) is prog.PytestReportEnvPropList:
                # If value is a list, recurse
                assert type(a_item.value) is prog.PytestReportEnvPropList
                __class__.compare_prop_lists(a_item.value, e_item.value)
            elif type(e_item.value) is str:
                assert type(a_item.value) is str
                # If value is a primitive (str, etc.)
                assert a_item.value == e_item.value
            else:
                # Internal error
                assert False, "type: {}".format(type(e_item.value).__name__)
            continue
        return
