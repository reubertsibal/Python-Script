# GitLab Active Users Exporter

This Python script allows you to fetch active users from a GitLab instance using the GitLab API and export their information to an Excel file.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3 installed on your system
- Required Python libraries installed: `requests` and `pandas`. You can install them using pip:

```bash
pip install requests pandas or pip3 install requests pandas
```

## Usage

Open the active-gitlab-user.py file in a text editor.

Replace the placeholder values in the script with your GitLab API token and GitLab URL:

api_token: Replace "test" with your GitLab API token.
gitlab_url: Replace "https://git.growsari.com/" with your GitLab instance URL.
Save the changes.

Run the script using the following command:
```
python active-gitlab-user.py
```

The script will fetch active users from your GitLab instance, create an Excel file named active_users.xlsx in the current directory, and save the users' information in the file.
