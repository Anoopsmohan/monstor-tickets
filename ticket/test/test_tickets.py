# -*- coding: utf-8 -*-
"""
    test_tickets

    Test the tickets API

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import unittest
from urllib import urlencode

import tornado
from tornado import testing, options
from monstor.app import make_app
from tickets.ticket.models import User, Ticket
from tickets.settings import SETTINGS
from monstor.utils.web import BaseHandler


class DummyHomeHandler(BaseHandler):
    """
    A dummy homepage
    """
    def get(self):
        self.write("Welcome Home")


class urls(object):
    """
    Fool monstor into believeing that this is an app folder and load the
    HANDLERS
    """
    HANDLERS = [
        tornado.web.URLSpec(r'/', DummyHomeHandler, name='home')
    ]


class TestTickets(testing.AsyncHTTPTestCase):

    def get_app(self):
        options.options.database = 'test_tickets'
        SETTINGS['xsrf_cookies'] = False
        SETTINGS['installed_apps'] = [
            'monstor.contrib.auth',
            'tickets.ticket',
            __name__,
        ]
        application = make_app(**SETTINGS)
        return application

    def setUp(self):
        super(TestTickets, self).setUp()
        user = User(name="Test User", email="test@example.com", active=True)
        user.set_password("password")
        user.save(safe=True)
        self.user = user

    def get_login_cookie(self):
        response = self.fetch(
            '/login', method="POST", follow_redirects=False,
            body=urlencode({
                'email': 'test@example.com', 'password': 'password'
            })
        )
        return response.headers.get('Set-Cookie')

    def test_0010_ticketlisthandler_get_1(self):
        """
        Test the TicketList handler without logged in
        """
        response = self.fetch(
            '/ticket-list', method="GET", follow_redirects=False
        )
        self.assertEqual(response.code, 302)

    def test_0020_ticketlisthandler_get_2(self):
        """
        Test the TicketList handler with logged in and HTML response with
        pagination (Render first page with 10 tickets)
        """

        for i in xrange(0, 100):
            ticket = Ticket(
                subject = "Testing",
                message = "Sample testing",
                status = "new",
                user = self.user,
                assigned_to = self.user,
                comment = []
            )
            ticket.save()

        response = self.fetch(
            '/ticket-list', method="GET", follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            }
        )
        self.assertEqual(response.code, 200)

    def test_0020_ticketlisthandler_get_3(self):
        """
        Test the TicketList handler with logged in and HTML response with
        pagination (Render fourth page with 10 elements)
        """

        for i in xrange(0, 100):
            ticket = Ticket(
                subject = "Testing",
                message = "Sample testing",
                status = "new",
                user = self.user,
                assigned_to = self.user,
                comment = []
            )
            ticket.save()

        response = self.fetch(
            '/ticket-list/4', method="GET", follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            }
        )
        self.assertEqual(response.code, 200)


    def test_0030_ticketlisthandler_get_4(self):
        """
        Test the TicketList handler with logged in and JSON response
        """
        response = self.fetch(
            '/ticket-list', method="GET", follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie(),
                'X-Requested-With': 'XMLHttpRequest',
            }
        )
        self.assertEqual(response.code, 200)

    def test_0040_tickethandler_get_1(self):
        """
        Test the Ticket handler get method without logged in
        """
        ticket = Ticket(
                subject = "Testing",
                message = "Sample testing",
                status = "new",
                user = self.user,
                assigned_to = self.user,
                comment = []
        )
        ticket.save()
        response = self.fetch(
            '/ticket/%s' % ticket.id,
            method="GET",
            follow_redirects=False,
        )
        self.assertEqual(response.code, 302)

    def test_0050_tickethandler_get_2(self):
        """
        Test the Ticket handler get method with logged in
        with correct ticket Id
        """
        ticket = Ticket(
                subject = "Testing",
                message = "Sample testing",
                status = "new",
                user = self.user,
                assigned_to = self.user,
                comment = []
        )
        ticket.save()
        response = self.fetch(
            '/ticket/%s' % ticket.id,
            method="GET",
            follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            },
        )
        self.assertEqual(response.code, 200)

    def test_0060_tickethandler_get_3(self):
        """
        Test the Ticket handler get method with wrong ticket Id
        """
        response = self.fetch(
            '/ticket/4fe1ae2655ca331d15000000',
            method="GET",
            follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            },
        )
        self.assertEqual(response.code, 302)

    def test_0070_tickethandler_get_4(self):
        """
        Test the Ticket handler get method without ticket id
        """
        response = self.fetch(
            '/ticket/+create-ticket',
            method="GET",
            follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            },
        )
        self.assertEqual(response.code, 200)

    def test_0080_tickethandler_post_1(self):
        """
        Test the TicketLists handler post method
        """
        response = self.fetch(
            '/ticket/+create-ticket', method="POST",
            follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            },
            body=urlencode({
                'subject':'testing',
                'message':'Sample testing',
                'status':'new',
                'assigned_to': str(self.user.id),
            })
        )
        self.assertEqual(response.code, 302)

    def test_0090_tickethandler_post_2(self):
        """
        Test the TicketLists handler post method without form field 'subject'
        """
        response = self.fetch(
            '/ticket/+create-ticket', method="POST",
            follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            },
            body=urlencode({
                'message':'Sample testing',
                'status':'new',
                'assigned_to': str(self.user.id),
            })
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(
            response.body.count(
                u'Something went wrong while saving your comment! Try Again'
            ), 1
        )

    def test_0100_ticketlisthandler_post_3(self):
        """
        Test the TicketLists handler post method without form field 'message'
        """
        response = self.fetch(
            '/ticket/+create-ticket', method="POST",
            follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            },
            body=urlencode({
                'subject':'testing',
                'status':'new',
                'assigned_to': str(self.user.id),
            })
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(
            response.body.count(
                u'Something went wrong while saving your comment! Try Again'
            ), 1
        )

    def test_0110_ticketlisthandler_post_4(self):
        """
        Test the TicketLists handler post method without form field 'status'
        """
        response = self.fetch(
            '/ticket/+create-ticket', method="POST",
            follow_redirects=False,
            headers={
                'Cookie': self.get_login_cookie()
            },
            body=urlencode({
                'message':'Sample testing',
                'subject':'testing',
                'assigned_to': str(self.user.id),
            })
        )
        self.assertEqual(response.code, 302)

    def test_0120_comment_handler_post_1(self):
        """
        Test the CommentHandler POST method
        """
        ticket = Ticket(
                subject = "Testing",
                message = "Sample testing",
                status = "new",
                user = self.user,
                assigned_to = self.user,
                comment = []
        )
        ticket.save()
        response = self.fetch(
            '/ticket/%s/comment' % ticket.id,
            method="POST",
            follow_redirects=False,
            body=urlencode({
                    'comment' : 'Tickets testing',
                    'status' : 'new',
            }),
            headers={
                'Cookie': self.get_login_cookie()
            },
        )
        self.assertEqual(response.code, 302)

    def test_0130_comment_handler_post_2(self):
        """
        Test the CommentHandler POST method, with invalid ticket id
        """
        response = self.fetch(
            '/ticket/4fe1ae2655ca331d15000000/comment',
            method="POST",
            follow_redirects=False,
            body=urlencode({
                    'comment' : 'Tickets testing'
            }),
            headers={
                'Cookie': self.get_login_cookie()
            },
        )
        self.assertEqual(response.code, 302)

    def test_0140_comment_handler_post_3(self):
        """
        Test the CommentHandler POST method, without 'comment' field
        """
        ticket = Ticket(
                subject = "Testing",
                message = "Sample testing",
                status = "new",
                user = self.user,
                assigned_to = self.user,
                comment = []
        )
        ticket.save()
        response = self.fetch(
            '/ticket/%s/comment' % ticket.id,
            method="POST",
            follow_redirects=False,
            body=urlencode({
            }),
            headers={
                'Cookie': self.get_login_cookie()
            },
        )
        self.assertEqual(response.code, 200)

    def tearDown(self):
        """
        Drop the database after every test
        """
        from mongoengine.connection import get_connection
        get_connection().drop_database('test_tickets')


if __name__ == '__main__':
    unittest.main()
