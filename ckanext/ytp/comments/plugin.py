import os
import ckan
import ckan.plugins as plugins
from ckan.plugins import implements, toolkit
from ckan.lib.plugins import DefaultTranslation
from ckan.common import _
import ckanext.ytp.comments.views as views
import ckanext.ytp.comments.command as ytp_cli
import ckanext.activity as activity
# import ckan.lib.activity_streams
import ckan.logic.validators

import logging

log = logging.getLogger(__name__)


# Monkey patch to add custom activity stream objects for comments
# log.warning("monkeypatching ckan.lib.activity_streams and ckan.logic.validators")

# def activity_stream_string_comment_added(context, activity):
#     return _("{actor} commented on {dataset}")
# ckan.lib.activity_streams.activity_stream_string_functions['comment added'] = activity_stream_string_comment_added
# ckan.lib.activity_streams.activity_stream_string_icons['comment added'] = 'comment'


# /Monkey patch


class YtpCommentsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    implements(plugins.IConfigurer)
    implements(plugins.IConfigurable)
    implements(plugins.IPackageController, inherit=True)
    implements(plugins.ITemplateHelpers, inherit=True)
    implements(plugins.IActions, inherit=True)
    implements(plugins.IAuthFunctions, inherit=True)
    implements(plugins.ITranslation)
    implements(plugins.IBlueprint)

    # IConfigurerable
    def configure(self, config):
        log.info("Configuring comments module")
        if hasattr(ckan, 'cli') and hasattr(ckan.cli, 'cli'):
            ckan.cli.cli.ckan.add_command(ytp_cli.ytp)
        if hasattr(activity, 'logic'):
            activity.logic.validators.object_id_validators['comment added'] = "package_id_exists"

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, "templates")
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('public/javascript/', 'comments_js')
        toolkit.add_resource('assets', 'ytp-comments')

    # ITranslation
    def i18n_directory(self):
        dn = os.path.dirname
        return os.path.join(dn(dn(dn(dn(os.path.abspath(__file__))))), 'i18n')

    def i18n_domain(self):
        return 'ckanext-ytp-comments'


    # IActions
    def get_actions(self):
        from ckanext.ytp.comments.logic.action import get, create, delete, update

        return {
            "comment_create": create.comment_create,
            "thread_show": get.thread_show,
            "comment_update": update.comment_update,
            "comment_show": get.comment_show,
            "comment_delete": delete.comment_delete,
            "comment_count": get.comment_count
        }

    # IAuthFunctions
    def get_auth_functions(self):
        from ckanext.ytp.comments.logic.auth import get, create, delete, update

        return {
            'comment_create': create.comment_create,
            'comment_update': update.comment_update,
            'comment_show': get.comment_show,
            'comment_delete': delete.comment_delete,
            "comment_count": get.comment_count
        }
        
    # IPackageController
    def before_dataset_view(self, pkg_dict):
        # TODO: append comments from model to pkg_dict
        return pkg_dict
    
    # IBlueprint
    def get_blueprint(self):
        # Create blueprints for all package types defined by other plugins.
        # Make sure this plugin is registered after them.
        all_package_types = set(['dataset'])
        for plugin in plugins.PluginImplementations(plugins.IDatasetForm):
            for package_type in plugin.package_types():
                all_package_types.add(package_type)
        return views.get_blueprints(all_package_types)

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_comment_thread': self._get_comment_thread,
            'get_comment_count_for_dataset': self._get_comment_count_for_dataset
        }
        
    def _get_comment_thread(self, dataset_name):
        import ckan.model as model
        from ckan.logic import get_action
        url = '/dataset/%s' % dataset_name
        return get_action('thread_show')({'model': model, 'with_deleted': True}, {'url': url})

    def _get_comment_count_for_dataset(self, dataset_name):
        import ckan.model as model
        from ckan.logic import get_action
        url = '/dataset/%s' % dataset_name
        count = get_action('comment_count')({'model': model}, {'url': url})
        return count
