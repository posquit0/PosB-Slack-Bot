#!/usr/bin/env python
# -*- coding: utf-8 -*-

from posb import SlackBot


def main():
    bot = SlackBot(
        'Your Token for Slack',
        'Channel to write',
        'Username'
    )

    # Add board to observe with a parameter `board_no`
    bot.add_board(3)
    bot.add_board(28)
    bot.add_board(14)
    bot.add_board(18)

    bot.set_timer(900)
    bot.work()

if __name__ == "__main__":
    main()
