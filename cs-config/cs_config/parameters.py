from typing import List
import paramtools
import marshmallow as ma


class Parameters(paramtools.Parameters):
    user_or_org: str
    cmds: List[str]
    ref: str
    title: str

    defaults = {
        "schema": {"operators": {"array_first": True}},
        "user_or_org": {
            "title": "GitHub User or Org",
            "description": "Username or title of GitHub repository.",
            "type": "str",
            "value": "hdoupe",
            "validators": {
                "choice": {
                    "choices": [
                        "hdoupe",
                        "jdebacker",
                        "Peter-Metz",
                        "PSLmodels",
                        "rickecon",
                    ]
                }
            },
        },
        "title": {
            "title": "Git Repository Title",
            "description": "Title of Git repository to clone.",
            "type": "str",
            "value": "ParamTools",
            "validators": {
                "choice": {
                    "choices": [
                        "Cost-of-Capital-Calculator",
                        "OG-USA",
                        "ParamTools",
                        "Tax-Calculator",
                        "Tax-Cruncher",
                    ]
                }
            },
        },
        "ref": {
            "title": "Git Reference or Branch.",
            "description": "Branch or commit ref to checkout.",
            "type": "str",
            "value": "master",
        },
        "cmds": {
            "title": "Test Commands",
            "description": "Extra Test Commands.",
            "type": "str",
            "number_dims": 1,
            "value": ["py.test . -v"],
        },
    }
