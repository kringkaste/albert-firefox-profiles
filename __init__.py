# -*- coding: utf-8 -*-

"""
Launch Firefox with one of the available profiles.
"""

import os
import configparser
from albert import *
from pathlib import Path

md_iid = "2.0"
md_version = "1.0"
md_name = "Firefox Profile Launcher"
md_description = "Launch Firefox with one of the available profiles."
md_license = "MIT"
md_url = "https://github.com/kringkaste/albert-firefox-profiles"


class Plugin(PluginInstance, GlobalQueryHandler):

    def __init__(self):
        GlobalQueryHandler.__init__(
            self,
            id=md_id,
            name=md_name,
            description=md_description,
            defaultTrigger="ff ",
        )
        PluginInstance.__init__(self, extensions=[self])

    def handleGlobalQuery(self, query):
        home = Path.home()
        plugin_dir = Path(__file__).parent
        rank_items = []
        if os.path.isfile(home / ".mozilla" / "firefox" / "profiles.ini"):
            config = configparser.ConfigParser()
            config.read(home / ".mozilla" / "firefox" / "profiles.ini")
            for section in config.sections():
                if section.startswith("Profile"):
                    rank_items.append(
                        RankItem(
                            StandardItem(
                                id=section,
                                text=config[section]["Name"],
                                inputActionText=query.trigger + config[section]["Name"],
                                iconUrls=["file:" + str(plugin_dir / "firefox.png")],
                                actions=[
                                    Action(
                                        "Open",
                                        "Open %s" % config[section]["Name"],
                                        lambda profile=config[section][
                                            "Name"
                                        ]: runDetachedProcess(
                                            ["firefox", "-P", profile]
                                        ),
                                    )
                                ],
                            ),
                            1,
                        )
                    )
        else:
            rank_items.append(
                RankItem(
                    StandardItem(
                        id=md_id,
                        text="Not found",
                    ),
                    1,
                )
            )

        return rank_items
