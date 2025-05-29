import requests
from collections import defaultdict

# Optional: Add your GitHub personal access token here to avoid rate limits
GITHUB_TOKEN = "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"  # e.g., "ghp_XXXXXXXXXXXXXXXXXXXX"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def fetch_repositories(user_or_org, entity_type="users"):
    """
    Fetch repositories for a given user or organization.
    entity_type: "users" or "orgs"
    """
    url = f"https://api.github.com/{entity_type}/{user_or_org}/repos"
    repos = []
    page = 1

    while True:
        response = requests.get(url, headers=HEADERS, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos

def classify_by_language(repositories):
    """
    Classify and count repositories based on the programming language.
    """
    language_dict = defaultdict(list)

    for repo in repositories:
        language = repo['language'] or "Unknown"
        language_dict[language].append(repo['name'])

    return language_dict

def display_results(language_dict):
    print("\n=== Repository Language Classification ===\n")
    for language, repos in sorted(language_dict.items(), key=lambda x: -len(x[1])):
        print(f"{language} ({len(repos)} project(s)):")
        for repo in repos:
            print(f"  - {repo}")
        print()
# sample github organization( microsoft)
if __name__ == "__main__":
    user_or_org = input("Enter GitHub username or organization: ")
    entity_type = input("Is this a 'user' or an 'org'? (default: user): ").strip().lower() or "user"
    entity_type = "orgs" if entity_type == "org" else "users"

    repositories = fetch_repositories(user_or_org, entity_type)
    if not repositories:
        print("No repositories found or failed to fetch.")
    else:
        classified = classify_by_language(repositories)
        display_results(classified)
