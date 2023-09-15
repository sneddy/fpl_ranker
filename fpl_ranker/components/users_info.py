import os
from collections import defaultdict

from cached_property import cached_property

from fpl_ranker.components.players_info import PlayerInfo
from fpl_ranker.utils.network_utils import safe_request


class UserInfo():

    def __init__(self, entry: int, players_info: PlayerInfo, name: str = None, team: str = None):
        self.entry = str(entry)
        self.name = name
        self.team = team
        self.players_info = players_info
        self.event_body = f'https://fantasy.premierleague.com/api/entry/{entry}/event'
        self.event_storage = {}

    def _get_user_history(self):
        personal_body = "https://fantasy.premierleague.com/api/entry/"
        personal_suffix = "history"
        url = os.path.join(personal_body, str(self.entry), personal_suffix)
        data = safe_request(url)
        return data['current']

    def _get_event(self, event_id: int):
        event_id = str(event_id)
        if event_id in self.event_storage:
            return self.event_storage[event_id]
        url = os.path.join(self.event_body, event_id, 'picks')
        self.event_storage[event_id] = safe_request(url)
        return self.event_storage[event_id]

    def _get_picks_info(self, event_id):
        picks = self._get_event(event_id)['picks']
        pick_info = defaultdict(list)
        for pick in picks:
            player_id = pick['element']
            name = self.players_info.id2name_dict[player_id]
            if pick['is_captain']:
                pick_info['captain'] = name
            if pick['multiplier'] != 0:
                position = self.players_info.id2pos_dict[player_id]
                pick_info[position].append(name)
            else:
                pick_info['bench'].append(name)
        for pos in self.players_info.positions:
            pick_info[pos] = ', '.join(sorted(pick_info[pos]))
        pick_info['bench'] = ', '.join(sorted(pick_info['bench']))
        return pick_info

    def _get_event_summary(self, event_id):
        data = self._get_event(event_id)
        summary = {
            'entry': self.entry,
            'team_name': self.team,
            'user_name': self.name,
            'active_chip': data['active_chip'],
            'points': data['entry_history']['points'],
            'event_transfers': data['entry_history']['event_transfers'],
            'event_transfers_cost': data['entry_history']['event_transfers_cost']
        }
        summary['pure_points'] = summary['points'] - summary['event_transfers_cost']
        picks_info = self._get_picks_info(event_id)
        summary.update(picks_info)
        return summary

    @cached_property
    def history_summary(self):
        history = self._get_user_history()
        summary = {'team_name': self.team, 'user_name': self.name}
        prev_points = 0
        for event_row in history:
            event_id = event_row['event']
            summary[f'gw_{event_id}'] = event_row['total_points'] - prev_points
            prev_points = event_row['total_points']
        return summary