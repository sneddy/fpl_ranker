import os

import pandas as pd
import transliterate
from PIL import Image, ImageDraw, ImageFont


class ImageDrawer():
    def __init__(self, template_path: str, font_path: str):
        self.template_path = template_path
        self.font_path = font_path
    
    def _get_template(self):
        return Image.open(self.template_path).resize((900, 900))
    
    def draw_event_league(self, league_name: str, event_df: pd.DataFrame):
        """
        event_df: ['entry', 'team_name', 'user_name', 'active_chip',
            'points', 'total_points', 'event_transfers', 'event_transfers_cost',
            'bank', 'pure_points', 'gk', 'def', 'mid', 'captain', 'frw', 'bench']
        """
        leaderboard_top_margin = 100
        item_height = 20
        img_height = leaderboard_top_margin + item_height * (event_df.shape[0] + 1)
        img = self._get_template().resize((1900, img_height))
        
        mega_title_font = ImageFont.truetype(self.font_path, 40)
        default_font = ImageFont.truetype(self.font_path, 16)
        players_font = ImageFont.truetype(self.font_path, 12)
        
        title_color = (255, 0, 0)
        team_color = (255, 255, 0)
        score_color = (255, 255, 255)
        
        draw = ImageDraw.Draw(img)
        text_position = (700, 25)
        draw.text(text_position, league_name, fill=team_color, font=mega_title_font)

        # draw titles
        title_top_margin = 80
        text_position = (100, title_top_margin)
        draw.text(text_position, 'Name', fill=title_color, font=default_font)
        text_position = (290, title_top_margin)
        draw.text(text_position, 'Total', fill=title_color, font=default_font)
        text_position = (345, title_top_margin)
        draw.text(text_position, 'GW', fill=title_color, font=default_font)
        text_position = (380, title_top_margin)
        draw.text(text_position, 'Cost', fill=title_color, font=default_font)
        text_position = (425, title_top_margin)
        draw.text(text_position, 'Chips', fill=title_color, font=default_font)
        text_position = (510, title_top_margin)
        draw.text(text_position, 'Captain', fill=title_color, font=default_font)
        text_position = (660, title_top_margin)
        draw.text(text_position, 'GK', fill=title_color, font=default_font)
        text_position = (850, title_top_margin)
        draw.text(text_position, 'Defenders', fill=title_color, font=default_font)
        text_position = (1250, title_top_margin)
        draw.text(text_position, 'Midfielders', fill=title_color, font=default_font)
        text_position = (1660, title_top_margin)
        draw.text(text_position, 'Forwards', fill=title_color, font=default_font)

        # draw leaderboard
        for idx, row in event_df.sort_values('total_points').iterrows():
            # position
            text_position = (20, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, str(idx), fill=score_color, font=default_font)
            # team name
            text_position = (50, leaderboard_top_margin + idx * item_height)
            user_name = transliterate.translit(row['user_name'], "ru", reversed=True)
            draw.text(text_position, user_name, fill=team_color, font=default_font)
            # new total
            text_position = (300, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, str(row['total_points']), fill=score_color, font=default_font)
            # new score
            text_position = (350, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, str(row['pure_points']), fill=score_color, font=default_font)
            # transfers cost
            text_position = (390, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, str(row['event_transfers_cost']), fill=score_color, font=default_font)
            # chips
            text_position = (410, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, str(row['active_chip']).replace('nan', ''), fill=score_color, font=default_font)
            # captain
            text_position = (500, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, row['captain'], fill=score_color, font=players_font)
            # gk
            text_position = (610, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, row['gk'], fill=score_color, font=players_font)
             # def
            text_position = (750, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, row['def'], fill=score_color, font=players_font)
             # mid
            text_position = (1100, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, row['mid'], fill=score_color, font=players_font)
             # frw
            text_position = (1630, leaderboard_top_margin + idx * item_height)
            draw.text(text_position, row['frw'], fill=score_color, font=players_font)

        return img

    
    def draw_league_of_leagues(self, leagues_summary):
        img = self._get_template()
        
        mega_title_font = ImageFont.truetype(self.font_path, 40)
        default_font = ImageFont.truetype(self.font_path, 16)
        title_font = ImageFont.truetype(self.font_path, 20)
        
        title_color = (255, 0, 0)
        team_color = (255, 255, 0)
        score_color = (255, 255, 255)
        
        draw = ImageDraw.Draw(img)
        text_position = (80, 100)
        draw.text(text_position, 'League of leagues by average score', fill=team_color, font=mega_title_font)

        # draw titles
        title_top_margin = 200
        text_position = (110, title_top_margin)
        draw.text(text_position, 'League', fill=title_color, font=title_font)
        text_position = (290, title_top_margin)
        draw.text(text_position, 'GW4', fill=title_color, font=title_font)
        text_position = (370, title_top_margin)
        draw.text(text_position, 'Total', fill=title_color, font=title_font)
        text_position = (570, title_top_margin)
        draw.text(text_position, 'MVP', fill=title_color, font=title_font)
        text_position = (750, title_top_margin)
        draw.text(text_position, 'MVPScore', fill=title_color, font=title_font)
        
        # draw leaderboard
        leaderboard_top_margin = 250
        for idx, row in leagues_summary.iterrows():
            # position
            text_position = (20, leaderboard_top_margin + idx * 50)
            old_team_position = row['old_position']
            team_position = f'{idx + 1} ({old_team_position})' 
            draw.text(text_position, team_position, fill=score_color, font=default_font)

            # logo
            logo_position = (95, leaderboard_top_margin + idx * 50)
            logo_path = f'misc/logo/' + row['league_name']
            logo_path = logo_path + '.png' if os.path.exists(logo_path + '.png') else logo_path + '.jpg'
            logo = Image.open(logo_path).resize((25, 25))
            img.paste(logo, logo_position)
            # league name
            text_position = (125, leaderboard_top_margin + idx * 50)
            draw.text(text_position, row['league_name'], fill=team_color, font=default_font)
            # new score
            text_position = (300, leaderboard_top_margin + idx * 50)
            draw.text(text_position, str(row['new_score']), fill=score_color, font=default_font)
            # new total
            text_position = (390, leaderboard_top_margin + idx * 50)
            draw.text(text_position, str(row['new_total_score']), fill=score_color, font=default_font)
            # mvp names
            text_position = (490, leaderboard_top_margin + idx * 50)
            draw.text(text_position, str(row['mvp_names']), fill=score_color, font=default_font)
            # mvp scores
            text_position = (815, leaderboard_top_margin + idx * 50)
            draw.text(text_position, str(row['mvp_score']), fill=score_color, font=default_font)
        return img