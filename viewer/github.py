from dataclasses import dataclass

import requests
from funcy import post_processing


@dataclass
class GithubUserData:
    login: str
    avatar_url: str


@dataclass
class GithubRepo:
    title: str
    url: str


@dataclass
class GithubClient:
    """
    Returns None, when request is not successfull.
    """

    access_token: str

    def get_user_data(self):
        response = requests.get(
            "https://api.github.com/user", headers=self._request_headers()
        )
        if response.status_code != 200:
            return None
        else:
            return GithubUserData(
                login=response.json()["login"],
                avatar_url=response.json()["avatar_url"],
            )

    @post_processing(list)
    def get_repos(self, user_data: GithubUserData):
        url = 'https://api.github.com/users/{}/repos'.format(user_data.login)
        response = requests.get(url, headers=self._request_headers())
        if response.status_code != 200:
            return None
        else:
            for item in response.json():
                yield GithubRepo(
                    title=item['full_name'],
                    url=item['html_url'],
                )

    def _request_headers(self):
        return {'Authorization': 'token {}'.format(self.access_token)}
