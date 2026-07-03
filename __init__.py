# -*- coding: utf-8 -*-

"""
Launch Firefox with one of the available profiles.
"""

import os
import configparser
from albert import *
from pathlib import Path

md_iid = "5.0"
md_version = "1.0.0"
md_name = "Firefox Profile Launcher"
md_description = "Launch Firefox with one of the available profiles."
md_license = "MIT"
md_url = "https://github.com/kringkaste/albert-firefox-profiles"
md_authors = ["@kringkaste"]
md_maintainers = ["@kringkaste"]


class Plugin(PluginInstance, GlobalQueryHandler):

    def __init__(self):
        PluginInstance.__init__(self)
        GlobalQueryHandler.__init__(self)

    def configWidget(self):
        return [{ 'type': 'label', 'text': __doc__.strip() }]

    def defaultTrigger(self):
        return 'ff '

    @staticmethod
    def makeIcon():
        return Icon.image(Path(__file__).parent / "firefox.png")

    def rankItems(self, query):
        home = Path.home()
        rank_items = []
        matcher = Matcher(query.query)

        if os.path.isfile(home / ".mozilla" / "firefox" / "profiles.ini"):
            config = configparser.ConfigParser()
            config.read(home / ".mozilla" / "firefox" / "profiles.ini")
            for section in config.sections():
                if section.startswith("Profile"):
                    if m := matcher.match(config[section]["Name"]):
                        rank_items.append(
                            RankItem(
                                StandardItem(
                                    id=section,
                                    text=config[section]["Name"],
                                    icon_factory=self.makeIcon,
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
                        id="no_profiles",
                        text="No profiles found",
                    ),
                    1,
                )
            )

        return rank_items
