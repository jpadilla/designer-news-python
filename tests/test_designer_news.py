import unittest
import mock

from designer_news import DesignerNews


class DesignerNewsTestCase(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch('designer_news.DesignerNews.Endpoint._request')
        self.mocked_requests = self.patcher.start()

        self.client_id = '<client_id_goes_here>'
        self.client_secret = '<client_secret_goes_here>'

        self.access_token = 'USER_SECRET_ACCESS_TOKEN'

        self.dn = DesignerNews(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token=self.access_token)

    def tearDown(self):
        self.patcher.stop()

    @mock.patch('designer_news.requests')
    def test_authenticate(self, mocked_requests):
        def mocked_json():
            return {
                "access_token": self.access_token,
                "token_type": "bearer",
                "scope": "user"
            }

        mocked_requests.post.return_value.json = mocked_json

        dn = DesignerNews(
            client_id=self.client_id, client_secret=self.client_secret)

        dn.authenticate(username='user', password='password')

        self.assertIsNotNone(dn.access_token)
        self.assertEqual(dn.access_token, self.access_token)

    def test_user_information(self):
        mocked_response = {
            "me": {
                "created_at": "2012-11-15T04:48:45Z",
                "first_name": "Kelly",
                "job": "Founder at LayerVault",
                "last_name": "Sutton",
                "portrait_url": "https://news.layervault.com/cats.gif"
            }
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.me()
        self.assertTrue('me' in response)

    def test_stories(self):
        mocked_response = {
            "story": {
                "comment": "",
                "comments": [],
                "created_at": "2014-01-24T17:15:19Z",
                "id": 13627,
                "site_url": "http://localhost:3000/stories/13627",
                "title": "A logo should tell a story.",
                "url": "http://localhost:3000/click/stories/13627",
                "vote_count": 11
            }
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.stories.get(1)
        self.assertTrue('story' in response)

    def test_stories_front_page(self):
        mocked_response = {
            "stories": [{
                "comment": "",
                "comments": [],
                "created_at": "2014-01-24T17:15:19Z",
                "id": 13627,
                "site_url": "http://localhost:3000/stories/13627",
                "title": "A logo should tell a story.",
                "url": "http://localhost:3000/click/stories/13627",
                "vote_count": 11
            }]
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.stories.front_page({'page': 1})
        self.assertTrue('stories' in response)
        self.assertEqual(len(response['stories']), 1)

    def test_stories_recent(self):
        mocked_response = {
            "stories": [{
                "comment": "",
                "comments": [],
                "created_at": "2014-01-24T17:15:19Z",
                "id": 13627,
                "site_url": "http://localhost:3000/stories/13627",
                "title": "A logo should tell a story.",
                "url": "http://localhost:3000/click/stories/13627",
                "vote_count": 11
            }]
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.stories.recent({'page': 1})
        self.assertTrue('stories' in response)
        self.assertEqual(len(response['stories']), 1)

    def test_stories_search(self):
        mocked_response = {
            "stories": [{
                "comment": "",
                "comments": [],
                "created_at": "2014-01-24T17:15:19Z",
                "id": 13627,
                "site_url": "http://localhost:3000/stories/13627",
                "title": "A logo should tell a story.",
                "url": "http://localhost:3000/click/stories/13627",
                "vote_count": 11
            }]
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.stories.search('Kelly Sutton')
        self.assertTrue('stories' in response)
        self.assertEqual(len(response['stories']), 1)

    def test_stories_upvote(self):
        mocked_get = {
            "stories": [{
                "comment": "",
                "comments": [],
                "created_at": "2014-01-24T17:15:19Z",
                "id": 13627,
                "site_url": "http://localhost:3000/stories/13627",
                "title": "A logo should tell a story.",
                "url": "http://localhost:3000/click/stories/13627",
                "vote_count": 11
            }]
        }

        self.mocked_requests.return_value = mocked_get

        response_get = self.dn.stories.get(13627)
        self.assertEqual(response_get['stories'][0]['vote_count'], 11)

        mocked_get['stories'][0]['vote_count'] += 1

        response_upvote = self.dn.stories.upvote(13627)
        self.assertEqual(response_upvote['stories'][0]['vote_count'], 12)

    def test_stories_reply(self):
        mocked_response = {
            "comment": {
                "body": "Kicking off the conversation.",
                "comments": [],
                "created_at": "2014-01-24T16:53:08Z",
                "depth": 0,
                "id": 9000,
                "vote_count": 0,
                "url": "https://news.layervault.com/comments/9000",
                "user_display_name": "Kelly S.",
                "user_id": 1
            }
        }

        self.mocked_requests.return_value = mocked_response

        comment = 'Kicking off the conversation.'
        response = self.dn.stories.reply(36524, comment)

        self.assertTrue('comment' in response)
        self.assertEqual(response['comment']['body'], comment)

    def test_comments_get(self):
        mocked_response = {
            "comment": {
                "body": "I would try something other than blue.",
                "comments": [],
                "created_at": "2014-01-24T16:53:08Z",
                "depth": 2,
                "id": 36524,
                "vote_count": 0,
                "url": "https://news.layervault.com/comments/36524",
                "user_display_name": "Matt P.",
                "user_id": 4181
            }
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.comments.get(36524)
        self.assertTrue('comment' in response)

    def test_comments_upvote(self):
        mocked_get = {
            "comment": {
                "body": "I would try something other than blue.",
                "comments": [],
                "created_at": "2014-01-24T16:53:08Z",
                "depth": 2,
                "id": 36524,
                "vote_count": 0,
                "url": "https://news.layervault.com/comments/36524",
                "user_display_name": "Matt P.",
                "user_id": 4181
            }
        }

        self.mocked_requests.return_value = mocked_get

        response_get = self.dn.comments.get(13627)
        self.assertEqual(response_get['comment']['vote_count'], 0)

        mocked_get['comment']['vote_count'] += 1

        response_upvote = self.dn.comments.upvote(36524)

        self.assertEqual(response_upvote['comment']['vote_count'], 1)

    def test_comments_reply(self):
        mocked_response = {
            "comment": {
                "body": "I agree. Purples are sweet.",
                "comments": [],
                "created_at": "2014-01-24T16:53:08Z",
                "depth": 3,
                "id": 9001,
                "vote_count": 0,
                "url": "https://news.layervault.com/comments/9001",
                "user_display_name": "Kelly S.",
                "user_id": 1
            }
        }

        self.mocked_requests.return_value = mocked_response

        comment = 'I agree. Purples are sweet.'
        response = self.dn.comments.reply(36524, comment)

        self.assertTrue('comment' in response)
        self.assertEqual(response['comment']['body'], comment)

    def test_motd_call(self):
        mocked_response = {
            "motd": {
                "downvote_count": 0,
                "message": "What was your first Mac? https://www.apple.com/",
                "upvote_count": 6,
                "user_display_name": "Wells R.",
                "user_id": 272
            }
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.motd()

        self.assertTrue('motd' in response)

    def test_motd_get(self):
        mocked_response = {
            "motd": {
                "downvote_count": 0,
                "message": "What was your first Mac? https://www.apple.com/",
                "upvote_count": 6,
                "user_display_name": "Wells R.",
                "user_id": 272
            }
        }

        self.mocked_requests.return_value = mocked_response

        response = self.dn.motd.get()

        self.assertTrue('motd' in response)

    def test_motd_upvote(self):
        mocked_response = {
            "motd": {
                "downvote_count": 0,
                "message": "What was your first Mac? https://www.apple.com/",
                "upvote_count": 6,
                "user_display_name": "Wells R.",
                "user_id": 272
            }
        }

        self.mocked_requests.return_value = mocked_response

        response_get = self.dn.motd()
        self.assertEqual(response_get['motd']['upvote_count'], 6)

        mocked_response['motd']['upvote_count'] += 1

        response_upvote = self.dn.motd.upvote()

        self.assertTrue('motd' in response_upvote)
        self.assertEqual(response_upvote['motd']['upvote_count'], 7)

    def test_motd_downvote(self):
        mocked_response = {
            "motd": {
                "downvote_count": 0,
                "message": "What was your first Mac? https://www.apple.com/",
                "upvote_count": 6,
                "user_display_name": "Wells R.",
                "user_id": 272
            }
        }

        self.mocked_requests.return_value = mocked_response

        response_get = self.dn.motd()
        self.assertEqual(response_get['motd']['downvote_count'], 0)

        mocked_response['motd']['downvote_count'] += 1

        response_upvote = self.dn.motd.downvote()

        self.assertTrue('motd' in response_upvote)
        self.assertEqual(response_upvote['motd']['downvote_count'], 1)
