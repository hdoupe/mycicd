from cs_config import functions
import cs_storage
from cs_storage.screenshot import write_template

"""
This script is useful to testing the outputs from the cs_config/functions.py
script.
"""


# outputs = functions.run_model(meta_param_dict, adjustment_dict)
outputs = functions.run_model(
    {},
    {
        "mycicd": {
            "title": "ParamTools",
            "user_or_org": "PSLmodels",
            "ref": "master",
            "cmds": ["py.test paramtools -v"],
        }
    },
)

i = 1
for output in outputs["renderable"]:
    serializer = cs_storage.get_serializer(output["media_type"])
    ser = serializer.serialize(output["data"])
    deserialized = dict(
        output, data=serializer.deserialize(ser, json_serializable=True)
    )
    deserialized["id"] = f"test-{i}"  # Need this output id.
    res = write_template(deserialized)
    with open(f"{output['title']}.html", "w") as f:
        f.write(res)
    i += 1
