from django.views.generic import TemplateView

from social_django.models import UserSocialAuth

from .github import GithubClient


class ViewAccount(TemplateView):
    template_name = 'view_account.html'

    def get_context_data(self, **kwargs):
        user_auth = UserSocialAuth.objects.get(user=self.request.user)
        access_token = user_auth.extra_data['access_token']
        client = GithubClient(access_token)
        user_data = client.get_user_data()
        return dict(user_data=user_data)
