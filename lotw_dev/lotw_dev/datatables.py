from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased, joinedload, subqueryload, contains_eager
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.util import get_distinct_values, icontains
from clld.db.models.common import Language, LanguageSource, Source
from clld.web.datatables.base import DataTable, Col, DetailsRowLinkCol, LinkCol
from clld.web.datatables.language import Languages
from clld.web.datatables.source import Sources
from clld.web.util.helpers import icon

from lotw_dev.models import (
    lotw_devLanguage, ClosureTable,

)




class NameCol(Col):
    def format(self, item):
        return item.name


class IsoCol(Col):
    def format(self, item):
        return item.iso

    def order(self):
        return lotw_devLanguage.iso

    def search(self, qs):
        iso_like = lotw_devLanguage.hid.op('~')('^[a-z]{3}$')
        return and_(lotw_devLanguage.hid.contains(qs.lower()), iso_like)


class FamilyCol(Col):
    def format(self, item):
        return item.family

class BranchCol(Col):
    def format(self, item):
        return item.branch

class Families(Languages):
    def __init__(self, req, model, **kw):
        self.type = kw.pop('type', req.params.get('type', 'languages'))
        super(Families, self).__init__(req, model, **kw)

    def default_order(self):
        return Language.updated.desc(), Language.pk

    def db_model(self):
        return lotw_devLanguage


    def col_defs(self):
        return [
            NameCol(self, 'name', model_col=Language.name, sTitle="Name"),
            IsoCol(self, 'iso', model_col=lotw_devLanguage.iso, sTitle='ISO-639-3'),
            FamilyCol(self, 'family', model_col=lotw_devLanguage.family, sTitle="Family"),
            BranchCol(self, 'branch', model_col=lotw_devLanguage.branch, sTitle="Branch"),
            Col(self, 'latitude'),
            Col(self, 'longitude'),
        ]

    def get_options(self):
        opts = super(Families, self).get_options()
        opts['sAjaxSource'] = self.req.route_url('languages', _query={'type': self.type})
        if self.type == 'families':
            opts['aaSorting'] = [[4, 'desc'], [0, 'asc']]
        return opts



def includeme(config):
    config.register_datatable("languages", Families)
