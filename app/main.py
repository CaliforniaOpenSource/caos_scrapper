import requests
import settings


def get_repos_with_criteria():
    url = 'https://api.github.com/search/repositories'
    headers = {'Authorization': settings.GITHUB_TOKEN}

    query_params = {
        'q': 'firmware language:C',
        'sort': 'stars',
        'order': 'desc'
    }
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        return []


repos = get_repos_with_criteria()
print(repos)
for repo in repos:
    print(f"Repository Name: {repo['name']}")
    print(f"Repository Owner: {repo['owner']}")
    print(f"Repository Created at: {repo['created_at']}")
    print(f"Repository Updated at: {repo['updated_at']}")
    print(f"Stars: {repo['stargazers_count']}")
    print(f"Forks: {repo['forks_count']}")
    print(f"License: {repo['license']['name'] if repo['license'] else 'No license specified'}")
    print(f"URL: {repo['html_url']}\n")
    print(f"Repository Name: {repo['description']}")
    print(f"Repository Name: {repo['topics']}")
    print(f"Repository Name: {repo['score']}")
