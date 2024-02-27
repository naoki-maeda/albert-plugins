"""
Access Git Repository with ghq.

Open Browser or VsCode.
"""

from pathlib import Path
from subprocess import run

from albert import *

md_iid = "2.0"
md_version = "1.0"
md_name = "Git Repository Access"
md_description = "Access Git Repository with ghq"
md_license = "MIT"
md_url = "https://github.com/naoki-maeda/albert-plugins"
md_maintainers = "@naoki-maeda"
md_bin_dependencies = ["rg", "ghq", "code"]


class Plugin(PluginInstance, TriggerQueryHandler):
    def __init__(self):
        TriggerQueryHandler.__init__(
            self,
            id=md_id,
            name=md_name,
            description=md_description,
            defaultTrigger='gh '
        )
        PluginInstance.__init__(self, extensions=[self])
        self.icon_url_github = [f"file:{Path(__file__).parent}/github-mark.svg"]
        self.icon_url_gitlab = [f"file:{Path(__file__).parent}/gitlab-logo-500.svg"]
        self.icon_url_vscode = [f"file:{Path(__file__).parent}/vscode.svg"]

    def synopsis(self):
        return "Enter Repository Search Text"

    def handleTriggerQuery(self, query):
        search_text = query.string.strip()
        if not search_text:
            return
        ghq_list = None
        ghq_root = None
        try:
            ghq_list = run(
                f"ghq list | rg {search_text}",
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
                item = StandardItem(
                    id=f"GitHub {gh}",
                    iconUrls=self.icon_url_github,
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
                item = StandardItem(
                    id=f"GitLab {gh}",
                    iconUrls=self.icon_url_gitlab,
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
            item = StandardItem(
                id=f"VsCode {gh}",
                iconUrls=self.icon_url_vscode,
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
