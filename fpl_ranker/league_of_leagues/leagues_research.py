import os
from typing import Dict, List

import pandas as pd
from cached_property import cached_property

import fpl_ranker.utils.string_utils as string_utils
from fpl_ranker.components.league_info import LeagueInfo
from fpl_ranker.components.players_info import PlayerInfo
from fpl_ranker.components.user_storage import UserStorage
from fpl_ranker.components.users_info import UserInfo


class LeaguesResearch:
    def __init__(
        self,
        leagues_list: List[int],
        event_id: int,
        old_scores: Dict[str, float],
        names_mapping: Dict[str, str],
        summary_dir: str = "artefacts",
    ):
        self.leagues_list = leagues_list
        self.event_id = event_id
        self.old_scores = old_scores
        self.names_mapping = names_mapping
        self.summary_dir = summary_dir
        os.makedirs(self.summary_dir, exist_ok=True)
        self.summary_path = os.path.join(self.summary_dir, f"summary.csv")
        self.players_info = PlayerInfo()
        self.user_storage = UserStorage(self.players_info)

    @cached_property
    def leagues_summary(self):
        summary_list = []
        for league_id in self.leagues_list:
            league_info = LeagueInfo(league_id)
            league_name = self.names_mapping.get(
                league_info.league_name, league_info.league_name
            )
            print(league_info.league_name)
            standings_filename = string_utils.to_filename(league_name) + ".csv"
            standings_fpath = os.path.join(self.summary_dir, standings_filename)
            if os.path.exists(standings_fpath):
                standings = pd.read_csv(standings_fpath)
            else:
                standings = league_info.get_event_standings(self.event_id, self.user_storage)
                standings.to_csv(standings_fpath)

            mvp_teams = standings.loc[
                standings.pure_points == standings["pure_points"].max(), "team_name"
            ]
            mvp_names = standings.loc[
                standings.pure_points == standings["pure_points"].max(), "user_name"
            ].tolist()
            mvp_names = [name.split()[0][0] + '. ' + name.split()[1] for name in mvp_names]
            league_summary = {
                "league_name": league_name,
                'n_teams': standings.shape[0],
                "old_total_score": self.old_scores[league_name],
                "new_score": standings["pure_points"].mean(),
                "mvp_score": standings["pure_points"].max(),
                "mvp_teams": ", ".join(mvp_teams.tolist()),
                "mvp_names": ", ".join(mvp_names),
            }
            summary_list.append(league_summary)
        summary_df = pd.DataFrame(summary_list)
        summary_df["new_total_score"] = (
            summary_df["old_total_score"] + summary_df["new_score"]
        ).round(2)
        summary_df["new_score"] = summary_df["new_score"].round(2)

        summary_df["old_position"] = (
            summary_df["old_total_score"]
            .rank(method="min", ascending=False)
            .astype(int)
        )
        summary_df["new_position"] = (
            summary_df["new_total_score"]
            .rank(method="min", ascending=False)
            .astype(int)
        )

        summary_df = summary_df.sort_values("new_position")
        summary_df.to_csv(self.summary_path, index=False)
        return summary_df

    def _get_league_link(self, league_id):
        return f"https://fantasy.premierleague.com/leagues/{league_id}/standings/c"

    def _prepare_text(self, league_id):
        link = self._get_league_link(league_id)
        name = "loh"
        return f"[{name}]({link})"

    def report(self):
        pass
