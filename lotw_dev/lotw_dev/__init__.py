from pyramid.config import Configurator
from functools import partial
from clld.web.app import menu_item

# we must make sure custom models are known at database initialization!
from lotw_dev import models


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('languages', partial(menu_item, 'languages', label='Languages')),
        ('features', partial(menu_item, 'parameters', label='Features')),
        ('references', partial(menu_item, 'sources', label='References')),
    )


    return config.make_wsgi_app()
