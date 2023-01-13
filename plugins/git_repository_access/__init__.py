"""
Access Git Repository with ghq.

Open Browser or VsCode.
"""

import os
from subprocess import run

from albert import *

md_iid = "0.5"
md_version = "1.0"
md_name = "Git Repository Access"
md_description = "Access Git Repository with ghq"
md_license = "MIT"
md_url = "https://github.com/naoki-maeda/albert-plugins"
md_maintainers = "@naoki-maeda"
md_bin_dependencies = ["grep", "ghq", "code"]

github_icon = [os.path.dirname(__file__) + "/github-mark.svg"]
gitlab_icon = [os.path.dirname(__file__) + "/gitlab-logo-500.svg"]
vscode_icon = [os.path.dirname(__file__) + "/vscode.svg"]


class Plugin(QueryHandler):
    def id(self):
        return __name__

    def name(self):
        return md_name

    def description(self):
        return md_description

    def defaultTrigger(self):
        return "gh "

    def synopsis(self):
        return "Enter Repository Search Text"

    def handleQuery(self, query):
        search_text = query.string.strip()
        if not search_text:
            return
        ghq_list = None
        ghq_root = None
        try:
            ghq_list = run(
                f"ghq list | grep {search_text}",
                capture_output=True,
                encoding="utf-8",
                check=True,
                shell=True,
            ).stdout.split("\n")
            ghq_root = run(
                "ghq root",
                capture_output=True,
                encoding="utf-8",
                check=True,
                shell=True,
            ).stdout.split("\n")[0]
        except Exception as e:
            warning(f"ghq error: {e}")

        if ghq_list is None or ghq_root is None:
            info(f"not found repository search text: {search_text}")
            return

        items = []
        for gh in ghq_list:
            if not gh:
                continue
            url = "https://" + gh
            project_path = f"{ghq_root}/{gh}"

            # GitHub Browser Open
            if gh.startswith("github.com"):
                item = Item(
                    id=f"GitHub {gh}",
                    icon=github_icon,
                    text=gh,
                    actions=[
                        Action(
                            id=f"Open GitHub {gh}",
                            text="Open GitHub",
                            callable=lambda url=url: openUrl(url=url),
                        ),
                    ],
                )
                items.append(item)

            # GitLab Browser Open
            elif gh.startswith("gitlab.com"):
                item = Item(
                    id=f"GitLab {gh}",
                    icon=gitlab_icon,
                    text=gh,
                    actions=[
                        Action(
                            id=f"Open GitLab {gh}",
                            text="Open GitLab",
                            callable=lambda url=url: openUrl(url=url),
                        ),
                    ],
                )
                items.append(item)

            # VsCode Folder Open
            item = Item(
                id=f"VsCode {gh}",
                icon=vscode_icon,
                text=gh,
                actions=[
                    Action(
                        id=f"Open VsCode {gh}",
                        text="Open VsCode",
                        callable=lambda project_path=project_path: runDetachedProcess(
                            ["code", "--folder-uri", project_path]
                        ),
                    ),
                ],
            )
            items.append(item)
        query.add(items)
