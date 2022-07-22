#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery

from .http_code import NotFoundException


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFoundException()
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            if description:
                raise NotFoundException(data=description)
            raise NotFoundException()
        return rv

    def paginate(self, page: int = None, per_page: int = None, **kwargs):
        """"""
        total = self.order_by(None).count()

        if page is None:
            page = 1

        if page < 1:
            page = 1

        if per_page < 1:
            per_page = 10

        if (total / per_page) == int(total / per_page):
            page_total = int(total / per_page)
        else:
            page_total = int(total / per_page) + 1

        if page == 1:
            page_num = 0
        else:
            page_num = per_page * page - per_page

        items = self.limit(per_page).offset(page_num).all()

        return dict(total=total, page_total=page_total, items=items, page=page, pagesize=len(items))


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True

    def __init__(self):
        pass

    def __getitem__(self, item):
        return getattr(self, item)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self
