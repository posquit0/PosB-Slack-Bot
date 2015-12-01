# Copyright 2015 Claud D. Park <posquit0.bj@gmail.com>

from slacker import Slacker
from time import sleep, localtime
import feedparser

RSS_URL = 'http://posb.postech.ac.kr/board/rss.jsp?board=%(board_id)d'
MESSAGE_FORMAT = 'PosB | %(title)s | (%(url)s)'


class Board(object):
    def __init__(self, id):
        self.id = id
        self.last_published = None


class SlackBot(object):
    def __init__(self, token, channel='#global', username='Bot', timer=600):
        self.token = token
        self.channel = channel
        self.username = username
        self.timer = timer
        self.boards = []

    def _send_message(self, msg):
        slack = Slacker(self.token)
        slack.chat.post_message(
            channel=self.channel,
            text=msg,
            username=self.username,
            as_user=False,
            icon_emoji=':new_moon_with_face:'
        )

    def set_token(self, token=None):
        self.token = token

    def set_channel(self, channel):
        self.channel = channel

    def set_username(self, username):
        self.username = username

    def set_timer(self, timer=1500):
        self.timer = timer

    def add_board(self, board_id):
        board = Board(board_id)
        self.boards.append(board)

    def work(self):
        while True:
            for board in self.boards:
                rss_url = RSS_URL % {'board_id': board.id}
                d = feedparser.parse(rss_url)
                articles = d['items'][::-1]
                unseen = []

                if board.last_published is None:
                    board.last_published = localtime()

                for article in articles:
                    published = article['published_parsed']
                    if published > board.last_published:
                        unseen.append(article)
                        board.last_published = published

                for article in unseen:
                    title = article['title']
                    published = article['published_parsed']
                    link = article['link']

                    msg = MESSAGE_FORMAT % {
                        'title': title,
                        'url': link
                    }
                    self._send_message(msg)

            sleep(self.timer)
