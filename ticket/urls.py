# -*- coding: utf-8 -*-
"""
    urls

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import tornado.web

from .views import(TicketListHandler, TicketHandler, CommentHandler)

U = tornado.web.URLSpec

HANDLERS = [
    U(r'/ticket-list', TicketListHandler, name="ticket.ticketlist-first"),
    U(r'/ticket-list/(\d+)', TicketListHandler, name="ticket.ticketlist"),
    U(r'/ticket/([a-zA-Z0-9-_]+)', TicketHandler,
        name="ticket.ticket" ),
    U(r'/ticket/\+create-ticket', TicketHandler,
        name="ticket.newticket"),
    U(r'/ticket/([a-zA-Z0-9-_]+)/comment', CommentHandler,
        name="ticket.ticket.comment")
]
