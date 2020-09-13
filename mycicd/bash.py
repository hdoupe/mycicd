from collections import namedtuple
import shlex
import subprocess
import sys
import time
from typing import List
import os


class CommandResult:
    def __init__(self, cmd, stderr, stdout, returncode):
        self.cmd = cmd
        self.stderr = stderr
        self.stdout = stdout
        self.returncode = returncode

    def __repr__(self):
        s = []
        s.append(f"$ {self.cmd}")
        s.append(self.stdout)
        if self.stderr:
            s.append(
                f"---------------------Error (returncode={self.returncode})------------------------"
            )
            s.append(self.stderr)
        return "\n".join(s)


class CommandFailed(Exception):
    def __init__(
        self,
        msg: str,
        cmd: CommandResult,
        prior_cmds: List[CommandResult],
        *args,
        **kwargs,
    ):
        self.msg = msg
        self.cmd = cmd
        self.prior_cmds = prior_cmds

    def __repr__(self):
        s = []
        if self.prior_cmds:
            for cmd in self.prior_cmds:
                s.append(repr(cmd))
        s.append(repr(self.cmd))
        return "\n".join(s)


def _run(cmd, conda_env=None):
    print(f"$ {cmd}")
    if conda_env is not None:
        env = {"PATH": f"/opt/conda/envs/{conda_env}/bin:$PATH"}
    else:
        env = None
    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
        executable="/bin/bash",
        shell=True,
        env=env,
    ) as p:
        stdout = ""
        for stdout_line in p.stdout:
            line = stdout_line.decode()
            stdout += line
            sys.stdout.write(line)
        _, stderr = p.communicate(timeout=None)
        returncode = p.poll()

    return CommandResult(
        cmd, stderr=stderr.decode(), stdout=stdout, returncode=returncode
    )


def run(cmd, batch=False, conda_env=None):
    if batch:
        cmds = cmd
    else:
        cmds = [cmd]

    results = []
    for cmd in cmds:
        result = _run(cmd, conda_env=conda_env)
        if result.returncode == 0:
            results.append(result)
        else:
            raise CommandFailed(result.stderr, result, results)

    if batch:
        return results
    else:
        return results[0]
