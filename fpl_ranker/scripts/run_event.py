from fpl_ranker.league_of_leagues.leagues_research import LeaguesResearch

if __name__ == "__main__":
    leagues_list = [
        579956,
        356774,
        406089,
        626932,
        5712,
        458888,
        406273,
        257622,
        180769,
        684405,
        381725,
        82273,
    ]

    names_mapping = {
        "Elite20KZ⭐️t.me/FPL_HQ": "Elite20KZ",
        "Classic TITANS & CHAMPIONSHIP": "Titans League",
        "World Class Fantasy League": "World Class League",
        "Тренерский ШТАБ | t.me/FPL_HQ": "Тренерский ШТАБ",
        "The_Best_Managers": "Best managers",
        "KZ FPL 2023/2024": "KZ FPL",
        "League-of-Legends": "League of Legends",
        "Zakynule FPL League": "Zakynule FPL League",
        "Classic Premier League": "Syndicate",
        "Keldibek's League": "Keldibek's League",
        "Open DSML League": "Open DSML League",
    }
    old_scores = {
        "Elite20KZ": 119.85,
        "Titans League": 117.7,
        "World Class League": 121.59,
        "Тренерский ШТАБ": 118.05,
        "Best managers": 120.63,
        "DV league": 119.39,
        "KZ FPL": 118.51,
        "League of Legends": 118.0,
        "Zakynule FPL League": 117.57,
        "Syndicate": 115.35,
        "Keldibek's League": 115.63,
        "Open DSML League": 110.66,
    }
    event_id = 4

    research = LeaguesResearch(
        leagues_list, event_id, old_scores, names_mapping, summary_dir="artefacts/gw4"
    )
    research.leagues_summary
