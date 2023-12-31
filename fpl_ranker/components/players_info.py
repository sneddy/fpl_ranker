import pandas as pd
from cached_property import cached_property

import fpl_ranker.utils.network_utils as network_utils


class PlayerInfo:
    def __init__(self):
        self.general_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        self.data = network_utils.safe_request(self.general_url)
        self.positions = ["gk", "def", "mid", "frw"]
        self.id2position = {1: "gk", 2: "def", 3: "mid", 4: "frw"}

    @cached_property
    def id2team_dict(self):
        return {elem["id"]: elem["name"] for elem in self.data["teams"]}

    @cached_property
    def summary(self):
        player_info = {}
        for elem in self.data["elements"]:
            player_id = elem["id"]
            name = elem["first_name"][0] + "." + elem["second_name"]
            player_info[player_id] = {
                "name": name,
                "team": self.id2team_dict[elem["team"]],
                "position": self.id2position[elem["element_type"]],
                "ownership": elem["selected_by_percent"],
                "total_points": elem["total_points"],
                "expected_goals": elem["expected_goals"],
                "expected_assists": elem["expected_assists"],
                "bonus": elem["bonus"],
                "cost": int(elem["now_cost"]) / 10,
                "transfers_in": elem["transfers_in"],
                "transfers_out": elem["transfers_out"],
            }
        player_info = pd.DataFrame(player_info).T.sort_values(
            "total_points", ascending=False
        )
        return player_info

    @cached_property
    def id2name_dict(self):
        return self.summary.name.to_dict()
    
    @cached_property
    def name2id_dict(self):
        return {name: idx for idx, name in self.id2name_dict.items()}

    def get_pos_by_name(self, name: str):
        return self.id2pos_dict[self.name2id_dict[name]]
    @cached_property
    def id2pos_dict(self):
        return self.summary.position.to_dict()
