import requests
import pandas as pd

def get_gitlab_users(api_token, gitlab_url):
    headers = {
        'Private-Token': api_token,
    }

    users_url = f"{gitlab_url}/api/v4/users"
    users = []

    page = 1
    while True:
        params = {'per_page': 100, 'page': page}
        response = requests.get(users_url, headers=headers, params=params)

        if response.status_code == 200:
            users_batch = response.json()
            if len(users_batch) == 0:
                break  # No more users to fetch
            users.extend(users_batch)
            page += 1
        else:
            print(f"Failed to fetch users. Status code: {response.status_code}")
            break

    return users

def main():
    api_token = "test"  # Your GitLab API token
    gitlab_url = "https://git.growsari.com/"  # Your GitLab URL

    users = get_gitlab_users(api_token, gitlab_url)

    active_users = [user for user in users if user['state'] == 'active']

    if active_users:
        print(f"Total {len(active_users)} active users found:")
        df = pd.DataFrame(active_users)
        df.to_excel("active_users.xlsx", index=False)
        print("Output saved to active_users.xlsx")
    else:
        print("No active users found.")

if __name__ == "__main__":
    main()
