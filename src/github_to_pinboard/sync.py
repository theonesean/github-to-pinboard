import requests
import os
import typer
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PINBOARD_TOKEN = os.getenv("PINBOARD_TOKEN")

GITHUB_API = f"https://api.github.com/users/{GITHUB_USERNAME}/starred"
PINBOARD_API = "https://api.pinboard.in/v1/posts/add"

def get_starred_repos(limit: int | None = None, verbose: bool = False):
    if not GITHUB_USERNAME or not GITHUB_TOKEN:
        typer.echo("Please set GITHUB_USERNAME and GITHUB_TOKEN in your environment variables.")
        raise typer.Exit(code=1)
    repos = []
    page = 1
    while True:
        if verbose:
            typer.echo(f"Fetching page {page} of starred repos from Github...")
        r = requests.get(GITHUB_API, auth=(GITHUB_USERNAME, GITHUB_TOKEN), params={"page": page, "per_page": 100})
        if r.status_code != 200:
            typer.echo(f"Github error: {r.status_code}")
            break
        page_repos = r.json()
        if not page_repos:
            if verbose:
                typer.echo("No more repos found.")
            break
        repos.extend(page_repos)
        if verbose:
            typer.echo(f"Fetched {len(page_repos)} repos (total so far: {len(repos)})")
        if limit and len(repos) >= limit:
            repos = repos[:limit]
            if verbose:
                typer.echo(f"Reached limit of {limit} repos.")
            break
        page += 1
    if verbose:
        typer.echo(f"Returning {len(repos)} repos.")
    return repos

def add_to_pinboard(repo, dry_run: bool = False, verbose: bool = False) -> bool:
    if not PINBOARD_TOKEN:
        typer.echo("Please set PINBOARD_TOKEN in your environment variables.")
        raise typer.Exit(code=1)

    url = repo["html_url"]
    title = repo["full_name"]
    description = repo.get("description", "")
    tags = "github starred"
    params = {
        "auth_token": PINBOARD_TOKEN,
        "url": url,
        "description": title,
        "extended": description,
        "tags": tags,
        "shared": "yes",
        "format": "json"
    }

    if verbose:
        typer.echo(f"Preparing to sync: {title}")
        typer.echo(f"Pinboard params: {params}")

    if dry_run:
        typer.echo(f"[DRY RUN] Would sync: {title}")
        return True

    r = requests.get(PINBOARD_API, params=params)
    if verbose:
        typer.echo(f"Pinboard response: {r.status_code} {r.text}")
    if r.status_code == 200:
        typer.echo(f"✅ Synced: {title}")
        return True
    else:
        typer.echo(f"❌ Failed to sync: {title} — {r.status_code} — {r.text}")
        return False

@app.command()
def sync(
    only_latest: int = typer.Option(None, help="Only sync the most recent N starred repos"),
    dry_run: bool = typer.Option(False, help="Simulate the sync without calling Pinboard"),
    verbose: bool = typer.Option(False, help="Show detailed output during sync"),
):
    """Sync Github starred repositories to Pinboard."""
    repos = get_starred_repos(limit=only_latest, verbose=verbose)
    success_count = 0

    for repo in repos:
        if verbose:
            typer.echo(f"Processing: {repo['full_name']} ({repo['html_url']})")
        if add_to_pinboard(repo, dry_run=dry_run, verbose=verbose):
            success_count += 1

    action = "would be" if dry_run else "were"
    typer.echo(f"\n✅ Completed. {success_count} bookmark{'s' if success_count != 1 else ''} {action} synced.")

if __name__ == "__main__":
    app()
