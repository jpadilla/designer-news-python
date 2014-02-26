"""
Python client library for the Designer News API.

This client library is designed to support v1 of the Designer News API.

Designer News API Reference: http://developers.news.layervault.com/.

This library provides a helper method to retrieve an access token using
a username and password flow. The suggested way for authenticating users
in your web applications is to use OAuth2. This library does not include
an oAuth2 client. Once you have an access token you can use it to initialize
the DesignerNews object.
"""
import inspect
import requests

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


__version__ = '0.1.0'
VERSION = __version__


BASE_ENDPOINT = 'https://api-news.layervault.com'
API_ENDPOINT = '{0}/api/v1'.format(BASE_ENDPOINT)


class DesignerNews(object):
    def __init__(self, client_id, client_secret, access_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

        # Initialize session with access token
        self._set_session()

        # Dynamically enable endpoints
        self._attach_endpoints()

    def _set_session(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer {0}'.format(self.access_token)
        })

    def _attach_endpoints(self):
        """
        Dynamically attach endpoint callables to this client.
        """
        for name, endpoint in inspect.getmembers(self):
            is_class = inspect.isclass(endpoint)
            is_subclass = is_class and issubclass(endpoint, self.Endpoint)
            not_endpoint = endpoint is not self.Endpoint

            if is_subclass and not_endpoint:
                endpoint_instance = endpoint(self.session)
                setattr(self, name.lower(), endpoint_instance)

    def authenticate(self, username, password):
        endpoint = '{0}/oauth/token'.format(BASE_ENDPOINT)

        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        r = requests.post(endpoint, data=payload)

        response = r.json()

        self.access_token = response['access_token']

        # Re-initialize session with access token
        self._set_session()

        # Dynamically enable endpoints
        self._attach_endpoints()

    class Endpoint(object):
        def __init__(self, session):
            self.session = session

        def _generate_url(self, path, params):
            if path:
                url = '{0}/{1}'.format(self.endpoint, path)
            else:
                url = '{0}'.format(self.endpoint)

            if params:
                url = '{0}?{1}'.format(url, urlencode(params))

            return '{0}/{1}'.format(API_ENDPOINT, url)

        def _request(self, method, url, payload=None):
            request = self.session.request(method, url, data=payload)

            try:
                return request.json()
            except ValueError:
                return request.raise_for_status()

        def get(self, path=None, params={}):
            url = self._generate_url(path, params)
            return self._request(method='GET', url=url)

        def post(self, path=None, params={}):
            url = self._generate_url(path, None)
            return self._request(method='POST', url=url, payload=params)

    class Me(Endpoint):
        endpoint = 'me'

        def __call__(self):
            return super(DesignerNews.Me, self).get()

    class Stories(Endpoint):
        endpoint = 'stories'

        def get(self, id):
            return super(DesignerNews.Stories, self).get(path=id)

        def front_page(self, params={}):
            return super(DesignerNews.Stories, self).get(params=params)

        def recent(self, params={}):
            return super(DesignerNews.Stories, self).get(
                path='recent', params=params)

        def search(self, query):
            return super(DesignerNews.Stories, self).get(
                path='search', params={'query': query})

        def upvote(self, id):
            return super(DesignerNews.Stories, self).post(
                path='{0}/upvote'.format(id))

        def reply(self, id, comment):
            return super(DesignerNews.Stories, self).post(
                path='{0}/reply'.format(id), params={'comment[body]': comment})

    class Comments(Endpoint):
        endpoint = 'comments'

        def get(self, id):
            return super(DesignerNews.Comments, self).get(path=id)

        def upvote(self, id):
            return super(DesignerNews.Comments, self).post(
                path='{0}/upvote'.format(id))

        def reply(self, id, comment):
            return super(DesignerNews.Comments, self).post(
                path='{0}/reply'.format(id), params={'comment[body]': comment})

    class MOTD(Endpoint):
        endpoint = 'motd'

        def __call__(self):
            return self.get()

        def get(self):
            return super(DesignerNews.MOTD, self).get()

        def upvote(self):
            return super(DesignerNews.MOTD, self).post(path='upvote')

        def downvote(self):
            return super(DesignerNews.MOTD, self).post(path='downvote')
