# Curling League Manager

A PyQt5 desktop application for managing curling leagues, teams, and team members. Data is stored in a simple JSON database file and can be imported/exported via CSV.

---

## Features

- **Main Window** — view and manage all leagues in the current database; load and save the database via file dialogs
- **League Editor** — view and manage teams within a league; import/export teams via CSV
- **Team Editor** — view and manage members within a team; add, update, and delete members
- Fully modal editor dialogs to keep the interface safe and consistent
- Persistent JSON storage with human-readable formatting
- CSV import/export for league data (teams + members)

---

## Project Structure

```
curling_league_manager/          ← top-level package
    __init__.py
    models/
        __init__.py
        member.py                ← Member data class
        team.py                  ← Team data class (contains Members)
        league.py                ← League data class (contains Teams)
        database.py              ← Database (contains Leagues), load/save JSON
    ui/
        __init__.py
        main_window.py           ← QMainWindow: league list, load/save DB
        league_editor.py         ← QDialog: team list, import/export CSV
        team_editor.py           ← QDialog: member list, add/update/delete
    utils/
        __init__.py
        csv_io.py                ← CSV import/export helpers
main.py                          ← Application entry point
requirements.txt
README.md
```

---

## Requirements

- Python 3.8 or higher
- PyQt5 5.15 or higher

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/curling-league-manager.git
   cd curling-league-manager
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

From the project root directory, run:

```bash
python main.py
```

---

## Usage Guide

### Main Window
- The main window shows all leagues in the currently loaded database.
- Use **File → Load Database** (or the **Load DB...** button) to open a saved `.json` database file.
- Use **File → Save Database** (or the **Save DB** button) to save the current database.
- Type a name in the text field and click **Add League** to create a new league.
- Select a league and click **Edit League** (or double-click it) to open the League Editor.
- Select a league and click **Delete League** to remove it.

### League Editor
- Shows all teams in the selected league.
- Use **League Data → Import from CSV** to import teams from a CSV file.
- Use **League Data → Export to CSV** to export the league's teams and members.
- Type a name and click **Add Team** to create a new team.
- Select a team and click **Edit Team** (or double-click) to open the Team Editor.
- Select a team and click **Delete Team** to remove it.

### Team Editor
- Shows all members in the selected team.
- Fill in the **Name** and **Email** fields, then click **Add Member** to add a new member.
- Select a member, edit the fields, and click **Update** to save changes.
- Select a member and click **Delete** to remove them.

### CSV Format

The CSV import/export uses the following column format:

```
team_name,member_name,member_email
Thunderstones,Alice Smith,alice@example.com
Thunderstones,Bob Jones,bob@example.com
Ice Breakers,Carol White,carol@example.com
```

Teams with no members can be represented with blank `member_name` and `member_email` columns.

---

## Database Format

The database is saved as a `.json` file:

```json
{
  "leagues": [
    {
      "name": "Winter League",
      "teams": [
        {
          "name": "Thunderstones",
          "members": [
            { "name": "Alice Smith", "email": "alice@example.com" }
          ]
        }
      ]
    }
  ]
}
```

---

## GitHub Setup

1. Create a new GitHub repository.
2. Push the project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Curling League Manager"
   git remote add origin https://github.com/<your-username>/curling-league-manager.git
   git push -u origin main
   ```
3. Invite collaborators via **Settings → Collaborators** in your GitHub repository.
