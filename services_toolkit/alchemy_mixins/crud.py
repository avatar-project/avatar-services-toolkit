from typing import Optional, Any

from flask_sqlalchemy import SQLAlchemy

from services_toolkit.alchemy_mixins.heplers import AttributedMixinBase


class CRUDMixin(AttributedMixinBase):
    def __new__(cls, db: SQLAlchemy):  # pylint: disable=arguments-differ
        return super(CRUDMixin, cls).__new__(cls,
                                             class_name='_CRUDMixin',
                                             parent_classes=(CRUDBase,), _db=db)


class CRUDBase:

    _db: Optional[SQLAlchemy] = None

    @classmethod
    def ensure(cls,
               **kwargs):
        instance = cls.read(**kwargs)
        return instance if instance is not None else cls.create(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        kwargs = cls._preprocess_params(**kwargs)
        instance = cls(**kwargs)  # noqa
        cls._db.session.add(instance)
        cls._db.session.commit()
        return instance

    @classmethod
    def all(cls, **kwargs):
        kwargs = cls._preprocess_params(**kwargs)
        return cls.query.filter_by(**kwargs).all()  # pylint: disable=no-member

    @classmethod
    def read(cls, **kwargs):
        kwargs = cls._preprocess_params(**kwargs)
        return cls.query.filter_by(**kwargs).first()  # pylint: disable=no-member

    def update(self, **kwargs):
        kwargs = self._preprocess_params(**kwargs)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self._db.session.commit()

    def save(self):
        self._db.session.add(self)
        self._db.session.flush()

    @classmethod
    def delete(cls, **kwargs):
        kwargs = cls._preprocess_params(**kwargs)
        rec = cls.read(**kwargs)
        cls._db.session.delete(rec)
        cls._db.session.commit()

    @staticmethod
    def _preprocess_params(**kwargs: Any) -> dict:
        return kwargs
