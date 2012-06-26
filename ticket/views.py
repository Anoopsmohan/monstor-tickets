# -*- coding: utf-8 -*-
"""
    views

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import tornado
from wtforms import Form, StringField, SelectField
from monstor.utils.wtforms import REQUIRED_VALIDATOR, TornadoMultiDict
from monstor.utils.web import BaseHandler, Pagination
from monstor.utils.i18n import _

from .models import Ticket, Comment


class TicketForm(Form):
    """
    Generate Form for creating Tickets
    """
    subject = StringField("subject", [REQUIRED_VALIDATOR])
    message = StringField('message', [REQUIRED_VALIDATOR])
    status = SelectField('status', [REQUIRED_VALIDATOR], default="new",
        choices=[
            ('new', 'New'),
            ('progress', 'Progress'),
            ('closed', 'Closed'),
        ]
    )


class CommentForm(Form):
    """
    Form to add comments to ticket.
    """
    comment = StringField("comment", [REQUIRED_VALIDATOR])
    status = SelectField('status', [REQUIRED_VALIDATOR],
        choices=[
            ('new', 'New'),
            ('progress', 'Progress'),
            ('closed', 'Closed'),
        ]
    )


class TicketListHandler(BaseHandler):
    """
    Handler for Tickets
    """
    @tornado.web.authenticated
    def get(self, page=1):
        """
        Render all tickets
        """
        tickets_qs = Ticket.objects(user=self.current_user)
        tickets = Pagination(int(page), 10, tickets_qs)
        if self.is_xhr:
            self.write({
                'result': [
                    {
                        'id': ticket.id,
                        'subject': ticket.subject,
                        'message': ticket.message,
                        'user': ticket.user,
                        'status': ticket.status,
                        'comments': ticket.comments,
                        'assigned_to' : ticket.assigned_to,
                    } for ticket in tickets
                ]
            })
        else:
            self.render(
                'ticket/ticket_list.html', tickets=tickets,
            )


class TicketHandler(BaseHandler):
    """
    Handler for a particuler ticket
    """
    @tornado.web.authenticated
    def get(self, ticket_id=None):
        """
        Render specified ticket
        """
        if ticket_id:
            ticket = Ticket.objects(
                id=ticket_id, user=self.current_user
            ).first()
            if not ticket:
                self.flash(_('Ticket not found!'), 'warning')
                self.redirect(self.get_argument('next', None) or \
                    self.reverse_url('home'))
                return

            if self.is_xhr:
                self.write({
                    'id': ticket.id,
                    'subject': ticket.subject,
                    'message': ticket.message,
                    'user': ticket.user,
                    'status': ticket.status,
                    'comments': ticket.comments,
                    'assigned_to' : ticket.assigned_to,
                })
            else:
                self.render(
                    'ticket/ticket.html', ticket=ticket
                )
        else:
            form = TicketForm()
            self.render(
                'ticket/ticket.html',
                ticket_form=TicketForm,
            )
        return

    @tornado.web.authenticated
    def post(self):
        form = TicketForm(TornadoMultiDict(self))
        if form.validate():
            ticket = Ticket(
                subject = form.subject.data,
                message = form.message.data,
                status = form.status.data,
                user = self.current_user,
                comment = []
            )
            ticket.save()
            self.flash(_("Your ticket has been created"), "info")
            self.redirect(
                self.reverse_url("ticket.ticket", ticket.id)
            )
            return
        self.flash(
            _(
                "Something went wrong while saving your comment! Try Again"
            ), 'error'
        )
        self.render('ticket/ticket.html', ticket_form=form)


class CommentHandler(BaseHandler):
    """
    Ticket Comment Handler
    """
    @tornado.web.authenticated
    def post(self, ticket_id):
        """
        Add comment to ticket
        """
        ticket = Ticket.objects(id=ticket_id, user=self.current_user).first()
        if not ticket:
            self.flash('Requested ticket not found,', 'warning')
            self.redirect(
                self.get_argument('next', None) or self.reverse_url('home')
            )
            return
        form = CommentForm(TornadoMultiDict(self))
        if form.validate():
            comment = Comment(
                comment=form.comment.data, user=self.current_user,
                status=form.status.data
            )
            if not ticket.comments:
                ticket.comments = [comment]
            else:
                ticket.comments.append(comment)
            ticket.save()
            self.flash(
                _("Your comment has been added to the ticket"), "Info"
            )
            self.redirect(
                self.reverse_url("ticket.ticket", ticket_id)
            )
        else:
            self.flash(
                _(
                    "Something went wrong while saving your comment! Try Again"
                ), "warning"
            )
            self.render('ticket/ticket.html', ticket=ticket)
            return

