from django.views.generic import TemplateView

from social_django.models import UserSocialAuth

from .github import GithubClient


class ViewAccount(TemplateView):
    template_name = 'view_account.html'

    def get_context_data(self, **kwargs):
        access_token = self._get_access_token()
        if access_token is not None:
            client = GithubClient(access_token)
            user_data = client.get_user_data()
            if user_data is None:
                repos = []
            else:
                repos = client.get_repos(user_data)
            return dict(user_data=user_data, repos=repos)
        else:
            return dict()

    def _get_access_token(self):
        if self.request.user.is_authenticated:
            # XXX: We always can to this, cuz users
            #      are always logged in with github
            user_auth = UserSocialAuth.objects.get(user=self.request.user)
            return user_auth.extra_data['access_token']
        else:
            return None