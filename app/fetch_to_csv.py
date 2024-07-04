import requests
import csv
import settings


def get_repos_with_criteria(min_stars=100, min_forks=150, language='Python', max_results=100):
    url = 'https://api.github.com/search/repositories'
    headers = {'Authorization': settings.GITHUB_TOKEN}  # Ensure your GitHub token is safely stored in settings.py
    query_params = {
        'q': 'firmware language:C',
        'sort': 'stars',
        'order': 'desc',
        'per_page': max_results  # Limits the number of results per page
    }
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        return []


def save_to_csv(repos, filename='repositories.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing the headers
        writer.writerow(
            ['Repository Name', 'Owner', 'Created At', 'Updated At', 'Stars', 'Forks', 'URL', 'Description', 'Topics',
             'Score', 'License'])
        # Writing the data
        for repo in repos:
            owner = repo['owner']['login'] if repo['owner'] else 'No owner'
            created_at = repo['created_at']
            updated_at = repo['updated_at']
            stars = repo['stargazers_count']
            forks = repo['forks_count']
            url = repo['html_url']
            description = repo['description'] if repo['description'] else 'No description'
            topics = ', '.join(repo['topics']) if repo['topics'] else 'No topics'
            score = repo['score']
            license_name = repo['license']['name'] if repo['license'] else 'No license specified'
            writer.writerow([repo['name'], owner, created_at, updated_at, stars, forks, url, description, topics, score,
                             license_name])


# Main execution flow
repos = get_repos_with_criteria()
save_to_csv(repos)
