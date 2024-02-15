import logging
import click

@click.group(short_help=u"ytp comments commands.")
def ytp():
    pass

@ytp.command()
def initdb():
    """
    Initialises the database with the required tables
    Connects to the CKAN database and creates the comment
    and thread tables ready for use.
    """
    log = logging.getLogger(__name__)
    log.info("starting command")

    import ckan.model as model
    model.Session.remove()
    model.Session.configure(bind=model.meta.engine)

    import ckanext.ytp.comments.model as cmodel
    log.info("Initializing tables")
    cmodel.init_tables()
    log.info("DB tables are setup")
