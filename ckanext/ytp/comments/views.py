import logging

from flask import Blueprint
from flask.views import MethodView
from typing import Any, cast, Optional, Union, Dict

import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import ckan.model as model
import ckan.lib.helpers as h
import ckan.lib.base as base
import ckan.lib.navl.dictization_functions as dict_fns

from ckan.common import _, c, request, current_user
from ckan.types import Context, Response

log = logging.getLogger(__name__)


ValidationError = logic.ValidationError
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
get_action = logic.get_action
check_access = logic.check_access



def add(dataset_id):
    return _add_or_reply(dataset_id)

def edit(dataset_id, comment_id):

    context = {'model': model, 'user': c.user}

    # Auth check to make sure the user can see this package

    data_dict = {'id': dataset_id}
    check_access('package_show', context, data_dict)

    try:
        c.pkg_dict = get_action('package_show')(context, {'id': dataset_id})
        c.pkg = context['package']
    except:
        return base.abort(403)

    data_dict = clean_dict(dict_fns.unflatten(
        tuplize_dict(parse_params(request.POST))))
    data_dict['id'] = comment_id
    success = False
    try:
        res = get_action('comment_update')(context, data_dict)
        success = True
    except ValidationError as ve:
        log.debug(ve)
    except Exception as e:
        log.debug(e)
        return base.abort(403)

    if success:
        return h.redirect_to(str('/dataset/%s#comment_%s' % (c.pkg.name, res['id'])))     
    return h.redirect_to(str('/dataset/%s' % c.pkg.name))                                   

def reply(dataset_id, parent_id):
    c.action = 'reply'

    try:
        data = {'id': parent_id}
        c.parent_dict = get_action("comment_show")({'model': model, 'user': c.user},
                                                    data)
        c.parent = data['comment']
    except:
        return base.abort(404)

    return _add_or_reply(dataset_id)

def delete(dataset_id, comment_id):

    context = {'model': model, 'user': c.user}

    # Auth check to make sure the user can see this package

    data_dict = {'id': dataset_id}
    check_access('package_show', context, data_dict)

    try:
        c.pkg_dict = get_action('package_show')(context, {'id': dataset_id})
        c.pkg = context['package']
    except:
        return base.abort(403)

    try:
        data_dict = {'id': comment_id}
        get_action('comment_delete')(context, data_dict)
    except Exception as e:
        log.debug(e)

    return h.redirect_to(str('/dataset/%s' % c.pkg.name))


def _add_or_reply(dataset_id):
    """
    Allows the user to add a comment to an existing dataset
    """
    context = {'model': model, 'user': c.user}

    # Auth check to make sure the user can see this package

    data_dict = {'id': dataset_id}
    check_access('package_show', context, data_dict)

    try:
        c.pkg_dict = get_action('package_show')(context, {'id': dataset_id})
        c.pkg = context['package']
    except:
        return base.abort(403)

    data_dict = clean_dict(dict_fns.unflatten(
        tuplize_dict(parse_params(request.form))))
    print(data_dict)
    data_dict['parent_id'] = c.parent.id if hasattr(c, 'parent') else None
    data_dict['url'] = '/dataset/%s' % c.pkg.name
    success = False
    try:
        res = get_action('comment_create')(context, data_dict)
        success = True
    except ValidationError as ve:
        log.debug(ve)
    except Exception as e:
        log.debug(e)
        return base.abort(403)

    if success:

        # add activity stream
        context.update({
            'ignore_auth': True
        })
        activity_data = {
            'user_id':c.user,
            "object_id": dataset_id,
            "activity_type": "comment added",
            "data": {
                "package": c.pkg_dict
            }
        }
        get_action('activity_create')(context, activity_data)

        return h.redirect_to(str('/dataset/%s#comment_%s' % (c.pkg.name, res['id'])))

    return h.redirect_to(str('/dataset/%s' % c.pkg.name))


def get_blueprints(all_package_types):
    blueprints = []

    for package_type in all_package_types:
        
        comment_blueprint = Blueprint(
            f'ytp_comments_{package_type}',
            __name__,
            url_prefix=f'/{package_type}',
        )


        comment_blueprint.add_url_rule(
            '/<dataset_id>/comments/add',
            view_func=add, methods=('POST', )
        )

        comment_blueprint.add_url_rule(
            '/<dataset_id>/comments/<comment_id>/edit',
            view_func=edit, methods=('POST', )
        )

        comment_blueprint.add_url_rule(
            '/<dataset_id>/comments/<parent_id>/reply',
            view_func=reply, methods=('POST', )
        )

        comment_blueprint.add_url_rule(
            '/<dataset_id>/comments/<comment_id>/delete',
            view_func=delete, methods=('GET', )
        )
        blueprints.append(comment_blueprint)
    
    return blueprints