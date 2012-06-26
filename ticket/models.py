# -*- coding: utf-8 -*-
"""
    models

    :copyright: (c) 2012 by Openlabs Technologies & Consulting (P) LTD
    :license: BSD, see LICENSE for more details.
"""
from mongoengine import (Document, EmbeddedDocument, StringField,
    ReferenceField, ListField, EmbeddedDocumentField)
from monstor.utils.i18n import _
from monstor.contrib.auth.models import User


STATUS_CHOICES = [
    ('new', 'New'),
    ('progress', 'Progress'),
    ('closed', 'Closed'),
]


class Comment(EmbeddedDocument):
    """
    Model for comments
    """
    user = ReferenceField(User, required=True, verbose_name=_("User"))
    comment = StringField(required=True, verbose_name=_("Comment"))
    status = StringField(
        required=True, verbose_name=_("Status"), choices=STATUS_CHOICES
    )


class Ticket(Document):
    """
    Model for tickets
    """
    subject = StringField(required=True, verbose_name=_("Subject"))
    message = StringField(required=True, verbose_name=_("Message"))
    user = ReferenceField(User, required=True, verbose_name=_("User"))
    assigned_to = ReferenceField(
        User, verbose_name=_("Assigned To")
    )
    status = StringField(
        required=True, verbose_name=_("Status"), choices=STATUS_CHOICES,
        default="new"
    )
    comments = ListField(
        EmbeddedDocumentField(Comment), verbose_name=_("comments")
    )

