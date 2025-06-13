# Github Starred to Pinboard Sync Script

This script syncs your starred repositories from Github to your [Pinboard](https://pinboard.in) account. It uses the Github API to fetch starred repos and the Pinboard API to save them as bookmarks. It is built with [Poetry](https://python-poetry.org/) and uses [Typer](https://typer.tiangolo.com/) for the CLI.

## Getting Started

1. **Install dependencies**
   ```bash
   poetry install
   ```

2. **Create a `.env` file** in the root directory with the following variables:
   ```env
   GITHUB_USERNAME=your_github_username
   GITHUB_TOKEN=your_github_token  # Needs `public_repo` scope at minimum
   PINBOARD_TOKEN=username:API_token  # Get it at https://pinboard.in/settings/password
   ```

3. **Run the sync script**
   ```bash
   poetry run python src/github_to_pinboard/sync.py
   ```

## CLI Options

- `--dry-run`: Simulate the sync without creating or updating any bookmarks.
- `--only-latest <N>`: Only process the latest N starred repositories.
- `--verbose`: If set, the script will print detailed information about what it is doing (API calls, parameters, responses, etc).

Example:
```bash
poetry run python src/github_to_pinboard/sync.py --only-latest 5 --dry-run
```

## Running Automatically with Cron

You can automate syncing by setting up a cron job. Example: sync every 15 minutes.

```cron
*/15 * * * * cd /path/to/github_to_pinboard && poetry run python src/github_to_pinboard/sync.py >> /tmp/github_sync.log 2>&1
```

> Make sure `poetry` is available in your shell's PATH when run from cron.

A sample cron job entry using Github Actions is also available in the `.github/workflows/sync.yml` file. (Note that Github's secrets can't start with `GITHUB_`, so they're named `GH_USERNAME` and `GH_TOKEN` in that file.)

## Shell Completion (Optional)

To enable shell tab completion for the CLI:
```bash
poetry run python src/github_to_pinboard/sync.py --install-completion
```

This enables autocompletion in `bash`, `zsh`, `fish`, or PowerShell.

## Development Notes

- Built using:
  - `requests` for HTTP requests
  - `python-dotenv` for environment variable management
  - `typer` for CLI interface

- No local state is stored: the script is stateless and safe to re-run.
- Pinboard deduplicates by URL, so bookmarks are either created or updated.

---

PRs welcome! Licensed under the Hippocratic License HL3-FULL.
