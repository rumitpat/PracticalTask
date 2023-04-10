import json
import os

import tweepy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.views.generic import ListView

from account.models import Profile


class TwitterListView(LoginRequiredMixin, ListView):
    template_name = 'twitter/tweets.html'
    context_object_name = 'twitter_posts'
    paginate_by = 6

    def get_queryset(self):
        API_KEY = os.environ.get('API_KEY')
        API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
        ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
        ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        genre = f"#{self.request.user.profile.genre}"
        WOEID = 23424848

        top_trends = api.get_place_trends(WOEID, include_entities=True, q=genre)

        tweets = []
        for trend in top_trends[0]['trends'][:10]:
            tweet = api.search_tweets(q=trend['name'], count=1, result_type='popular')
            if tweet and tweet[0].favorite_count:
                tweet = tweet[0]
                tweet_data = {
                    'name': tweet.user.name,
                    'screen_name': tweet.user.screen_name,
                    'profile_image_url': tweet.user.profile_image_url_https,
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat(),
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count
                }
                tweets.append(tweet_data)
        tweets_json = json.dumps(tweets, default=str)
        print(tweets_json)
        return tweets_json

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tweets_json = self.get_queryset()
        tweets = json.loads(tweets_json)
        page_number = self.request.GET.get('page')
        paginator = Paginator(tweets, self.paginate_by)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj
        return context
