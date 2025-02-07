from urllib.request import urlopen
import json
import tempdata


class Repos:
    def __init__(self, username):
        self.username = username
        self.url = 'https://api.github.com/users/' + self.username + '/repos'
        self.repos = {}
        self.data = {}
        self.all_languages = {}
        self.non_fork_languages = {}
        self.get_data()
        self.total_stars = 0

    def get_data(self):
        r = urlopen(self.url).read()
        # self.data = json.loads(r.decode('utf-8'))
        # reading from a cache for testing
        self.data = tempdata.data

    def get_repos_info(self):
        stars = 0
        for repo in self.data:
            self.repos[repo['name']] = {
                'created': repo['created_at'],
                'isfork': repo['fork'],
                'language': repo['language'],
                'stars': repo['stargazers_count'],
                'watchers': repo['watchers'],
                'forks': repo['forks']
            }
            if not repo['fork']:
                stars += repo['stargazers_count']

        self.total_stars = stars

    def languages_analysis(self):
        all_languages = {}
        non_fork_languages = {}
        repo_names = list(self.repos.keys())
        languageUrl = 'https://api.github.com/repos/' + self.username + '/'
        for i in repo_names:
            temp = urlopen(languageUrl + i + '/languages').read()
            lang_data = json.loads(temp.decode('utf-8'))
            if not self.repos[i]['isfork']:
                for lang in lang_data:
                    non_fork_languages[lang] = non_fork_languages.get(
                        lang, 0) + lang_data[lang]
            for lang in lang_data:
                all_languages[lang] = all_languages.get(
                    lang, 0) + lang_data[lang]

        self.all_languages = all_languages
        self.non_fork_languages = non_fork_languages


if __name__ == '__main__':
    test = Repos('Devyanshu')
    test.get_repos_info()
    test.languages_analysis()
