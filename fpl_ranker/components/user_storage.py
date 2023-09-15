from fpl_ranker.components.players_info import PlayerInfo
from fpl_ranker.components.users_info import UserInfo


class UserStorage():

    def __init__(self, players_info: PlayerInfo):
        self.storage = {}
        self.players_info = players_info

    def get(self, entry_id: int, name: str = None, team: str = None):
        if entry_id in self.storage:
            return self.storage[entry_id]
        self.storage[entry_id] = UserInfo(entry_id, self.players_info, name=name, team=team)
        return self.storage[entry_id]