from pathlib import Path
from datetime import datetime
import subprocess


def get_log_path():

    log_dir = (
        Path.home()
        / ".mle_support_agent"
    )

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return log_dir / "log.txt"


def get_repo_log_path():

    log_dir = (
        Path(__file__)
        .resolve()
        .parents[2]
        / "logs"
    )

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return log_dir / "log.txt"


def iso_timestamp():

    return (
        datetime.now()
        .astimezone()
        .isoformat()
    )


def get_repo_root():

    return str(
        Path(__file__)
        .resolve()
        .parents[2]
    )


def get_git_branch():

    try:

        return (
            subprocess.check_output(
                [
                    "git",
                    "rev-parse",
                    "--abbrev-ref",
                    "HEAD"
                ],
                text=True
            )
            .strip()
        )

    except Exception:

        return "unknown"


class PipelineLogger:

    def __init__(self):

        self.log_file = get_log_path()

        self.repo_log_file = (
            get_repo_log_path()
        )

    def _write_log(
        self,
        entry: str
    ):

        for path in [
            self.log_file,
            self.repo_log_file,
        ]:

            with open(
                path,
                "a",
                encoding="utf-8",
                newline="\n"
            ) as f:

                f.write(entry)

    def log_session_start(
        self,
        agent_name="support-agent"
    ):

        entry = f"""
## [{iso_timestamp()}] SESSION START

Agent: {agent_name}
Repo Root: {get_repo_root()}
Branch: {get_git_branch()}
Worktree: main
Parent Agent: none
Language: py

"""

        self._write_log(entry)

    def log_onboarding(
        self,
        agent_name="support-agent"
    ):

        entry = f"""
## [{iso_timestamp()}] ONBOARDING COMPLETE

AGREEMENT RECORDED: {get_repo_root()}
Agent: {agent_name}
Language: py
System Time: {iso_timestamp()}

"""

        self._write_log(entry)

    def log_turn(
        self,
        title,
        user_prompt,
        summary,
        actions=None,
        agent_name="support-agent"
    ):

        actions_text = "\n".join(
            f"* {a}"
            for a in (actions or [])
        )

        entry = f"""
## [{iso_timestamp()}] {title}

User Prompt (verbatim, secrets redacted):
{user_prompt}

Agent Response Summary:
{summary}

Actions:
{actions_text}

Context:
tool={agent_name}
branch={get_git_branch()}
repo_root={get_repo_root()}
worktree=main
parent_agent=none

"""

        self._write_log(entry)

    def log(
        self,
        message: str
    ):

        entry = (
            f"[{iso_timestamp()}] "
            f"{message}\n"
        )

        self._write_log(entry)
