import requests
import json
from datetime import datetime


def download_file(repo, path, user = "dnhansen", branch = "main"):
	file_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
	file_response = requests.get(file_url)
	with open(path, 'wb') as f:
		f.write(file_response.content)


download_file("cv", "cv.pdf")


# def get_commit_date(repo, user = "dnhansen", branch = "main"):
# 	commit_url = f"https://api.github.com/repos/{user}/{repo}/branches/{branch}"
# 	commit = requests.get(commit_url)
# 	commit_json = json.loads(commit.text)
# 	date_iso = commit_json["commit"]["commit"]["committer"]["date"]
# 	date = datetime.fromisoformat(date_iso)
# 	return date

# date = get_commit_date("comark")

# print(date.year, date.month, date.day)
