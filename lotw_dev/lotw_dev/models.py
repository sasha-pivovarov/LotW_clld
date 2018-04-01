from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.interfaces import IParameter, ILanguage
from clld.db.meta import Base, CustomModelMixin, DBSession
from clld.db.models.common import Language, Parameter


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(ILanguage)
class lotw_devLanguage(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    family = Column(String)
    branch = Column(String)
    iso = Column(String)

@implementer(IParameter)
class TreeFeature(Parameter, CustomModelMixin):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    father_pk = Column(Integer, ForeignKey('treefeature.pk'))

    def get_ancestors(self):
        # retrieve the ancestors ordered by distance, i.e. from direct parent
        # to top-level family:
        return DBSession.query(TreeFeature) \
            .join(TreeClosureTable, and_(
            TreeClosureTable.parent_pk == TreeFeature.pk,
            TreeClosureTable.depth > 0)) \
            .filter(TreeClosureTable.child_pk == self.pk) \
            .order_by(TreeClosureTable.depth)

class ClosureTable(Base):
    __table_args__ = (UniqueConstraint('parent_pk', 'child_pk'),)
    parent_pk = Column(Integer, ForeignKey('treefeature.pk'))
    child_pk = Column(Integer, ForeignKey('treefeature.pk'))
    depth = Column(Integer)
