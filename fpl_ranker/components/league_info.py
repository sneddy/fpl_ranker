import pandas as pd
from tqdm.auto import tqdm

import fpl_ranker.utils.network_utils as network_utils
from fpl_ranker.components.user_storage import UserStorage


class LeagueInfo:
    def __init__(self, league_id: int):
        self.league_id = league_id
        self.standings_body = "https://fantasy.premierleague.com/api/leagues-classic"
        self.league_name, self.members_info = self._get_basic_info()
        self.league_link = (
            f"https://fantasy.premierleague.com/leagues/{league_id}/standings/c"
        )

    def _get_basic_info(self, page: int = 1):
        standings_suffix = f"standings/?page_standings={page}"
        url = network_utils.url_join(
            self.standings_body, str(self.league_id), standings_suffix
        )
        data = network_utils.safe_request(url, 1)
        league_name = data["league"]["name"]
        members_info = data["standings"]["results"]

        keys_to_extract = ["entry", "player_name", "entry_name"]
        members_info = [
            {k: v for k, v in item.items() if k in keys_to_extract}
            for item in members_info
        ]
        if len(members_info) == 50:
            print("Make additional league query")
            _, tail = self._get_basic_info(page + 1)
            members_info.extend(tail)
        return league_name, members_info

    def get_event_standings(self, event_id, user_storage: UserStorage):
        standings = []
        for member in tqdm(self.members_info):
            user_info = user_storage.get(
                member["entry"], name=member["player_name"], team=member["entry_name"]
            )
            standings.append(user_info._get_event_summary(event_id))
        return pd.DataFrame(standings)

    def get_overall_standings(self, user_storage: UserStorage):
        standings = []
        for member in tqdm(self.members_info):
            user_info = user_storage.get(
                member["entry"], name=member["player_name"], team=member["entry_name"]
            )
            # user_info = UserInfo(member['entry'], players_info, name=member['player_name'], team=member['entry_name'])
            standings.append(user_info.history_summary)
        return pd.DataFrame(standings)
