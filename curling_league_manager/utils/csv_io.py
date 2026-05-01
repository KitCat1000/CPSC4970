"""
Nicole Tressler
April 21, 2026.
CPSC 4970, Auburn University

Final Project: PyQt5 Interface

"""

"""Utility functions for importing and exporting league data."""

import csv
from typing import List
from curling_league_manager.models.league import League
from curling_league_manager.models.team import Team
from curling_league_manager.models.member import Member


def export_league_csv(league: League, filepath: str):
    """
    Export a league to a CSV file.
    Format: team_name, member_name, member_email
    """
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["team_name", "member_name", "member_email"])
        for team in league.teams:
            if not team.members:
                writer.writerow([team.name, "", ""])
            else:
                for member in team.members:
                    writer.writerow([team.name, member.name, member.email])


def import_league_csv(filepath: str, league_name: str = None) -> League:
    """
    Import a league from a CSV file.
    Expected columns: team_name, member_name, member_email
    If league_name is not provided, uses the filename stem.
    """
    import os

    if league_name is None:
        league_name = os.path.splitext(os.path.basename(filepath))[0]

    league = League(name=league_name)
    teams: dict[str, Team] = {}

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team_name = row.get("team_name", "").strip()
            member_name = row.get("member_name", "").strip()
            member_email = row.get("member_email", "").strip()

            if not team_name:
                continue

            if team_name not in teams:
                team = Team(name=team_name)
                teams[team_name] = team
                league.add_team(team)

            if member_name:
                teams[team_name].add_member(Member(name=member_name, email=member_email))

    return league
