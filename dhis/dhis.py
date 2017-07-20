from . import session, BASE_URL
from .utils import clean_data
from pprint import pprint

def organisationUnits(query=None, paging='false', fields='name,code,level'):
    '''
    :param query:
    :param paging:
    :param fields:
    :return:
    '''
    params = {
        'paging': paging,
        'query': query,
        'fields': fields
    }
    path = BASE_URL + "organisationUnits.json"
    session.params = params
    response = session.get(path)
    return response.json()


def dataElements(query=None, paging='false', fields='name,code'):
    '''
    :param query:
    :param paging:
    :param fields:
    :return:
    '''
    params = {
        'paging': paging,
        'query': query,
        'fields': fields
    }
    path = BASE_URL + "dataElements.json"
    session.params = params
    response = session.get(path)
    return response.json()


def analytics(dx=None, ou=None, pe=None, co=None, ao=None, displayProperty='NAME', skipMeta='false',orgLevel=2):
    '''
    :param dx: the data element,indicator,dataset etc
    :param ou: organisationUnit IDs
    :param pe: ISO periods and relative periods
    :param co: Category option combinations
    :param ao: Attribute option combinations
    :param displayProperty: Property to display for metadata.
    :param skipMeta: Exclude the meta data part of the response (improves performance).
    :return:
    '''
    params = {
        'dimension': ['ou:' + ou, 'pe:' + pe],
        'filter': ['dx:' + dx],
        'displayProperty': displayProperty,
        'skipMeta': skipMeta
    }
    path = BASE_URL + "/25/analytics.json"
    session.params = params
    response = session.get(path)
    r= response.json()
    geojson = orgGeojson(level=orgLevel)
    data = clean_data(r,geojson)
    return data

def orgGeojson(level,parent=None):
    '''

    :param level: the OrganisationUnit levels,if more than one separated by comma in a string
    :param parent:
    :return:
    '''
    levels = str(level).split(',')
    params = {
        'level':[]
    }
    for level in levels:
        params['level'].append(level)

    path = BASE_URL + "organisationUnits.geojson"
    session.params = params
    response = session.get(path)
    return response.json()

