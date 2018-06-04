# -*- coding: utf-8 -*-
from Acquisition import aq_base
import base64
import sys
import pprint
import traceback

try:
    import simplejson as json
except:
    import json

from redturtle.exporter.base.browser.wrapper import Wrapper
from ploneorg.jsonify.jsonify import GetItem as BaseGetItemView
from ploneorg.jsonify.jsonify import GetChildren as BaseGetChildrenView
from .migration.topics import TopicMigrator
from plone import api
import DateTime
from plone.app.discussion.interfaces import IConversation


def _clean_dict(dct, error):
    new_dict = dct.copy()
    message = str(error)
    for key, value in dct.items():
        if message.startswith(repr(value)):
            del new_dict[key]
            return key, new_dict
    raise ValueError("Could not clean up object")


def get_json_object(self, context_dict):
    passed = False
    while not passed:
        try:
            JSON = json.dumps(context_dict)
            passed = True
        except Exception, error:
            if "serializable" in str(error):
                key, context_dict = _clean_dict(context_dict, error)
                pprint.pprint('Not serializable member %s of %s ignored'
                              % (key, repr(self)))
                passed = False
            else:
                return ('ERROR: Unknown error serializing object: %s' %
                        str(error))

    self.request.response.setHeader('Content-Type', 'application/json')
    return JSON


def get_discussion_objects(self, context_dict):
    conversation = IConversation(self.context)
    comments = conversation.getComments()
    comments = [comment for comment in comments]
    tmp_lst = []
    for item in comments:
        tmp_dict = item.__dict__
        if not tmp_dict.get('status'):
            states = tmp_dict['workflow_history'].values()
            comment_status = states[0][-1]['review_state']
        try:
            del tmp_dict['__parent__']
            del tmp_dict['workflow_history']
        except:
            pass
        tmp_dict['modification_date'] = DateTime.DateTime(
            tmp_dict['modification_date']).asdatetime().isoformat()
        tmp_dict['creation_date'] = DateTime.DateTime(
            tmp_dict['creation_date']).asdatetime().isoformat()
        if not tmp_dict.get('status'):
            tmp_dict.update({'status': comment_status})
        tmp_lst.append(tmp_dict)
    context_dict.update({'discussions': tmp_lst})


def get_solr_extrafields(self, context_dict):
    if not getattr(self.context, 'searchwords', None):
        return
    context_dict.update({'searchwords': self.context.searchwords.raw})


class GetItemSchedaER(BaseGetItemView, GetPortletsData):

    def __call__(self):
        """
        """
        try:
            context_dict = Wrapper(self.context)
            context_dict.update({'portlets_data': self.get_portlets_data()})
            get_discussion_objects(self, context_dict)
            get_solr_extrafields(self, context_dict)

            if context_dict.get('_type') == 'SchedaER':
                links_info = [
                    'toDeepen',
                    'rulesAndActs',
                    'modules',
                    'ongoingProjects',
                    'initiatives',
                    'publications',
                    'usefulLinks',
                    'seeOther'
                ]
                for item in links_info:
                    if getattr(self.context, item, None):
                        context_dict.update(
                            {item: getattr(self.context, item)})

        except Exception, e:
            tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
            return 'ERROR: exception wrapping object: %s\n%s' % (str(e), tb)

        return get_json_object(self, context_dict)


class GetItemBando(BaseGetItemView, GetPortletsData):

    def __call__(self):
        """
        """
        try:
            context_dict = Wrapper(self.context)
            context_dict.update({'portlets_data': self.get_portlets_data()})
            get_discussion_objects(self, context_dict)
            get_solr_extrafields(self, context_dict)

            closing_date = context_dict.get('chiusura_procedimento_bando', '')
            if closing_date:
                fixed_date = closing_date.split(' ')[0]
                context_dict.update(
                    {'chiusura_procedimento_bando': fixed_date})
            context_dict.update({'_layout': context_dict['_defaultpage']})
            context_dict.update({'_defaultpage': ''})
        except Exception, e:
            tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
            return 'ERROR: exception wrapping object: %s\n%s' % (str(e), tb)

        return get_json_object(self, context_dict)


class GetItemCircolare(BaseGetItemView, GetPortletsData):

    def __call__(self):
        """
        """
        try:
            context_dict = Wrapper(self.context)
            context_dict.update({'portlets_data': self.get_portlets_data()})
            get_discussion_objects(self, context_dict)
            get_solr_extrafields(self, context_dict)

            dataCircolare = context_dict.get('dataCircolare', '')
            if dataCircolare:
                fixed_date = dataCircolare.split(' ')[0]
                context_dict.update({'dataCircolare': fixed_date})

            if context_dict['_datafield_file2']['size'] == 0:
                del context_dict['_datafield_file2']

            if context_dict['_datafield_file3']['size'] == 0:
                del context_dict['_datafield_file3']

            if context_dict['_datafield_file1']['size'] == 0:
                del context_dict['_datafield_file1']

            context_dict.update({'_layout': context_dict['_defaultpage']})
            context_dict.update({'_defaultpage': ''})
        except Exception, e:
            tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
            return 'ERROR: exception wrapping object: %s\n%s' % (str(e), tb)

        return get_json_object(self, context_dict)


class GetItemBacheca(BaseGetItemView, GetPortletsData):

    def __call__(self):
        """
        """
        try:
            context_dict = Wrapper(self.context)
            context_dict.update({'portlets_data': self.get_portlets_data()})
            get_discussion_objects(self, context_dict)
            get_solr_extrafields(self, context_dict)

            context_dict['presentation_text'] = context_dict.get(
                'passaparolaPresentation'
            )
            del context_dict['passaparolaPresentation']

            context_dict['ads_help_text'] = context_dict.get(
                'passaparolaClassifiedText'
            )
            del context_dict['passaparolaClassifiedText']

            context_dict['privacy_text'] = context_dict.get(
                'passaparolaPrivacy'
            )
            del context_dict['passaparolaPrivacy']

            context_dict['select_type'] = 'Advertisement'

            context_dict['recipient_email'] = context_dict.get(
                'passaparolaRecipientEmail'
            )
            del context_dict['passaparolaRecipientEmail']

            context_dict['expiration_days'] = context_dict.get(
                'passaparolaExpirationDays'
            )
            del context_dict['passaparolaExpirationDays']

            context_dict.update({'_layout': context_dict['_defaultpage']})
            context_dict.update({'_defaultpage': ''})
        except Exception, e:
            tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
            return 'ERROR: exception wrapping object: %s\n%s' % (str(e), tb)

        return get_json_object(self, context_dict)


class GetItemAnnuncio(BaseGetItemView, GetPortletsData):

    def __call__(self):
        """
        """
        try:
            context_dict = Wrapper(self.context)
            context_dict.update({'portlets_data': self.get_portlets_data()})
            get_discussion_objects(self, context_dict)
            get_solr_extrafields(self, context_dict)

            context_dict['text'] = context_dict.get(
                'description'
            )
            del context_dict['description']

            context_dict['image'] = context_dict.get(
                '_datafield_image'
            )

            context_dict['additionalImage'] = context_dict.get(
                '_datafield_additionalimage'
            )

            context_dict['external_link'] = context_dict.get(
                'externalurl'
            )
            del context_dict['externalurl']

            context_dict.update({'_layout': context_dict['_defaultpage']})
            context_dict.update({'_defaultpage': ''})
        except Exception, e:
            tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
            return 'ERROR: exception wrapping object: %s\n%s' % (str(e), tb)

        return get_json_object(self, context_dict)


class GetItemBookCrossing(BaseGetItemView, GetPortletsData):

    def __call__(self):
        """
        """
        try:
            context_dict = Wrapper(self.context)
            context_dict.update({'portlets_data': self.get_portlets_data()})
            get_discussion_objects(self, context_dict)
            get_solr_extrafields(self, context_dict)

            context_dict['presentation_text'] = context_dict.get(
                'bookcrossingPresentation'
            )
            del context_dict['bookcrossingPresentation']

            context_dict['ads_help_text'] = context_dict.get(
                'bookcrossingHelpText'
            )
            del context_dict['bookcrossingHelpText']

            context_dict['privacy_text'] = context_dict.get(
                'bookcrossingPrivacy'
            )
            del context_dict['bookcrossingPrivacy']

            context_dict['select_type'] = 'BookCrossing'

            context_dict['recipient_email'] = context_dict.get(
                'bookcrossingRecipientEmail'
            )
            del context_dict['bookcrossingRecipientEmail']

            context_dict['expiration_days'] = context_dict.get(
                'bookcrossingExpirationDays'
            )
            del context_dict['bookcrossingExpirationDays']

            context_dict.update({'_layout': context_dict['_defaultpage']})
            context_dict.update({'_defaultpage': ''})
        except Exception, e:
            tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
            return 'ERROR: exception wrapping object: %s\n%s' % (str(e), tb)

        return get_json_object(self, context_dict)


class GetItemBookCrossingInsertion(BaseGetItemView, GetPortletsData):

    def __call__(self):
        """
        """
        try:
            context_dict = Wrapper(self.context)
            context_dict.update({'portlets_data': self.get_portlets_data()})
            get_discussion_objects(self, context_dict)
            get_solr_extrafields(self, context_dict)

            context_dict['text'] = context_dict.get(
                'insertionDescription'
            )
            del context_dict['insertionDescription']

            context_dict['image'] = context_dict.get(
                '_datafield_image'
            )

            context_dict['additionalImage'] = context_dict.get(
                '_datafield_additionalimage'
            )

            context_dict['author'] = context_dict.get(
                'insertionAuthor'
            )
            del context_dict['insertionAuthor']

            context_dict['exchange_method'] = context_dict.get(
                'insertionExchangeMethod'
            )
            del context_dict['insertionExchangeMethod']

            context_dict['genre'] = context_dict.get(
                'insertionGenre'
            )
            del context_dict['insertionGenre']

            context_dict.update({'_layout': context_dict['_defaultpage']})
            context_dict.update({'_defaultpage': ''})
        except Exception, e:
            tb = pprint.pformat(traceback.format_tb(sys.exc_info()[2]))
            return 'ERROR: exception wrapping object: %s\n%s' % (str(e), tb)

        return get_json_object(self, context_dict)
