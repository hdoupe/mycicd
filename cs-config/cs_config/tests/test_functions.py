from cs_kit import CoreTestFunctions

from cs_config import functions


class TestFunctions1(CoreTestFunctions):
    get_version = functions.get_version
    get_inputs = functions.get_inputs
    validate_inputs = functions.validate_inputs
    run_model = functions.run_model
    ok_adjustment = {
        "mycicd": {
            "title": "ParamTools",
            "user_or_org": "PSLmodels",
            "ref": "master",
            "cmds": ["py.test paramtools -v"],
        }
    }
    bad_adjustment = {
        "mycicd": {
            "title": "ParamTools",
            "user_or_org": "some-malicious-user",
            "ref": "master",
            "cmds": ["commence destruction"],
        }
    }  # your invalid inputs here
