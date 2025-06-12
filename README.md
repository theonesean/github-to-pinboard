# Github Starred to Pinboard sync script

This script syncs your starred repositories from GitHub to Pinboard.

## Getting Started

1. `poetry install`
2. Create a `.env` file in the root directory with the following content:
   ```
   GITHUB_USERNAME=your_github_username
   GITHUB_TOKEN=your_github_token
   PINBOARD_TOKEN=your_pinboard_token
   ```
3. Run the script:
   ```
   poetry run python src/github_to_pinboard/sync.py 
   ```

## Options

- `--dry-run`: If set, the script will not create any bookmarks in Pinboard, but will print what it would do.
- `--verbose`: If set, the script will print detailed information about what it is doing.
- `--only-latest <N>`: If set, the script will only process the latest N starred repositories.