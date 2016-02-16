# encoding: utf-8


# pandaSDMX is licensed under the Apache 2.0 license a copy of which
# is included in the source distribution of pandaSDMX.
# This is notwithstanding any licenses of third-party software included in
# this distribution.
# (c) 2014, 2015 Dr. Leo <fhaxbox66qgmail.com>


'''
pandaSDMX - a Python package for SDMX - Statistical Data and Metadata eXchange

'''


from pandasdmx.api import Request
import logging

__all__ = ['Request']

__version__ = '0.4a1'


def _init_logger():
    logger = logging.getLogger('pandasdmx')
    handler = logging.StreamHandler()
    fmt = logging.Formatter(
        '%(asctime)s %(name)s - %(levelname)s: %(message)s')
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)
    return logger

logger = _init_logger()


def odo_register():
    '''
    Enable conversion of .sdmx files with odo (http://odo.readthedocs.org).
    Adds conversion from sdmx to PD.DataFrame to odo graph.
    Note that native discovery of sdmx files is not yet supported. odo will thus 
    convert to PD.DataFrame
    and discover the data shape from there.
    '''
    logger.info('Registering with odo...')
    import odo
    from odo.utils import keywords
    import pandas as PD
    from toolz import keyfilter
    import toolz.curried.operator as op

    class PandaSDMX(object):

        def __init__(self, uri):
            self.uri = uri

    @odo.resource.register(r'.*\.sdmx')
    def _(uri, **kwargs):
        return PandaSDMX(uri)

    @odo.discover.register(PandaSDMX)
    def _(sdmx):
        # is there some metadata for the dtype?
        # if not just load the first couple of lines like a csv
        raise NotImplementedError('Discover of SDMX resources.')

    @odo.convert.register(PD.DataFrame, PandaSDMX)
    def _(sdmx, **kwargs):
        write = Request().get(fromfile=sdmx.uri).write
        return write(**keyfilter(op.contains(keywords(write)), kwargs))
    logger.info('odo registration complete.')
