# Write or import your Compute Studio functions here.
import mycicd
import requests

from .parameters import Parameters


def get_version():
    return mycicd.__version__


def get_inputs(meta_param_dict):
    return {"meta_parameters": {}, "model_parameters": {"mycicd": Parameters().dump()}}


def validate_inputs(meta_param_dict, adjustment, errors_warnings):
    params = Parameters()
    params.adjust(adjustment["mycicd"], raise_errors=False)

    errors_warnings["mycicd"].update({"errors": params.errors})
    if "ref" in adjustment["mycicd"]:
        try:
            resp = requests.get(
                f"https://github.com/{params.user_or_org}/{params.title}/tree/{params.ref}"
            )
            print(resp)
            if resp.status_code == 404:
                errors_warnings["mycicd"]["errors"]["ref"] = [
                    f"Unknown ref: {params.ref}"
                ]
        except Exception:
            errors_warnings["mycicd"]["errors"]["ref"] = [f"Invalid ref: {params.ref}"]

    return {"errors_warnings": errors_warnings}


def format_cmd(cmd):
    return f'<div style="text-align:left !important"><details open><summary>{cmd.cmd}</summary><pre><code>{str(cmd)}</code></pre></details></div>'


def run_model(meta_param_dict, adjustment):
    params = Parameters()
    params.adjust(adjustment["mycicd"])

    _, install_cmds, test_cmds = mycicd.cicd(
        user_or_org=params.user_or_org,
        title=params.title,
        ref=params.ref,
        test_cmd=params.cmds,
    )

    install_cmd_str = ""
    for cmd in install_cmds:
        install_cmd_str += format_cmd(cmd)

    test_cmd_str = ""
    for cmd in test_cmds:
        test_cmd_str += format_cmd(cmd)

    return {
        "renderable": [
            {"media_type": "table", "title": "Install Logs", "data": install_cmd_str,},
            {"media_type": "table", "title": "Test Logs", "data": test_cmd_str,},
        ],
        "downloadable": [],
    }
