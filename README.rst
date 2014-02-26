designer-news |Build Status|
============================

Python client library for the `Designer News API`_. Inspired by the
official `NodeJS client library`_ by LayerVault.

Install
-------

Using Github:

::

    git clone git@github.com:getblimp/blimp-python.git

Using pip:

::

    pip install blimp

Using easy\_install:

::

    easy_install blimp

Usage
-----

You can make authenticated requests in two ways.

Username and Password
~~~~~~~~~~~~~~~~~~~~~

::

    from designer_news import DesignerNews


    designer_news = DesignerNews(client_id, client_secret)
    designer_news.authenticate(username, password)
    designer_news.me()

Access Token
~~~~~~~~~~~~

The suggested way for authenticating users in your web applications is
to use OAuth2. This library does not include an oAuth2 client. `Read
more`_.

::

    from designer_news import DesignerNews


    designer_news = DesignerNews(client_id, client_secret, access_token)
    designer_news.me()

Available methods
-----------------

User
~~~~

::

    designer_news.me()

Stories
~~~~~~~

::

    designer_news.stories.get(story_id)
    designer_news.stories.front_page({'page': 1})
    designer_news.stories.recent({'page': 1})
    designer_news.stories.search(search_term')
    designer_news.stories.upvote(story_id)
    designer_news.stories.reply(story_id, comment_message)

Comments
~~~~~~~~

::

    designer_news.comments.get(comment_id)
    designer_news.comments.upvote(comment_id)
    designer_news.comments.reply(comment_id, comment_message)

MOTD
~~~~

::

    designer_news.motd()
    designer_news.motd.upvote()
    designer_news.motd.downvote()

License
-------

The MIT License (MIT)

Copyright (c) 2014 José Padilla

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. _Designer News API: http://developers.news.layervault.com/
.. _NodeJS client library: https://github.com/layervault/designer_news_js_client
.. _Read more: http://developers.news.layervault.com/#authentication-and-requesting-access-tokens

.. |Build Status| image:: https://travis-ci.org/jpadilla/designer-news-python.png?branch=master
   :target: https://travis-ci.org/jpadilla/designer-news-python