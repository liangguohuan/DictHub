#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import

import sqlite3
from .common import *


class DBBase(object):
    """
    docstring for DBBase
    """
    def __init__(self, path=''):
        super(DBBase, self).__init__()
        check_conf_dir()
        db_filename = DB_FILEPATH if path == '' or path != ':memory:' else path
        logger.info('db_filename is: %s' % db_filename)
        db_is_new = not os.path.exists(db_filename)

        conn = sqlite3.connect(db_filename)
        conn.isolation_level = None
        conn.row_factory = sqlite3.Row
        dbcur = conn.cursor()

        if db_is_new:
            logger.info('Create database at the first time.')
            with open(DB_SCHEME_FILEPATH, 'rt') as f:
                scheme = f.read()
            dbcur.executescript(scheme)
            logger.info('Create database is finished.')

        self.path = path
        self.conn = conn
        self.dbcur = dbcur

    @staticmethod
    def escape(string):
        return '`%s`' % string

    def execute(self, sql):
        logger.info('[EXECUTE] %s' % sql)
        self.dbcur.execute(sql)
        return self.dbcur

    def insert(self, tblname, fields, ignore=False):
        _keys = ', ' . join(map(lambda x: self.escape(x), fields.keys()))
        _values = ", ".join(['?', ] * len(fields))
        _ignore = 'OR IGNORE ' if ignore else ''
        sql = 'INSERT %s INTO %s(%s) VALUES (%s)' % (_ignore, self.escape(tblname), _keys, _values)
        logger.info('[INSERT] %s [bind] %s' % (sql, fields.values()))
        self.dbcur.execute(sql, list(fields.values()))
        logger.info('lastrowid is: %d' % self.dbcur.lastrowid)
        return self.dbcur.lastrowid

    def update(self, tblname, fields, where='1=0'):
        kwstr = ', '.join(['%s = "%s"' % (self.escape(k), v) for k, v in fields.items()])
        sql = 'UPDATE %s SET %s WHERE %s' % (self.escape(tblname), kwstr, where)
        logger.info('[UPDATE] %s' % sql)
        self.dbcur.execute(sql)
        return self.dbcur.rowcount

    def delete(self, tblname, where='1=0'):
        sql = 'DELETE FROM %s WHERE %s' % (self.escape(tblname), where)
        logger.info('[DELETE] %s' % sql)
        self.dbcur.execute(sql)
        return self.dbcur.rowcount

    def get(self, tblname, field='*', where='1=0'):
        _field = ', ' .join(map(lambda x: self.escape(x), field.split(','))) if field != '*' else field
        sql = 'SELECT %s FROM %s WHERE %s' % (_field, self.escape(tblname), where)
        logger.info('[GET] %s' % sql)
        self.dbcur.execute(sql)
        return self.dbcur.fetchone()

    def getlist(self, tblname, field='*', where='1=1', order='', limit='100'):
        _field = ', ' .join(map(lambda x: self.escape(x), field.split(','))) if field != '*' else field
        _order = ' ORDER BY %s' % order if order != '' else ''
        _limit = ' LIMIT %s' % limit if limit != '' else ''
        _where = where if where != '' else '1=1'
        sql = "SELECT %s FROM %s WHERE %s%s%s" % (_field, self.escape(tblname), _where, _order, _limit)
        logger.info('[SELECT] %s' % sql)
        self.dbcur.execute(sql)
        return self.dbcur


class TableBase(DBBase):
    """
    docstring for TableBase
    """
    __tablename__ = ''

    def __init__(self, path=''):
        if self.__tablename__ == '':
            from exceptions import AttributeError
            raise AttributeError('__tablename__ must be needed.')
        super(TableBase, self).__init__(path)

    def insert(self, fields, ignore=False):
        import time
        fields.update({'ctime': time.time()})
        return super(TableBase, self).insert(self.__tablename__, fields, ignore)

    def update(self, fields, where='1=0'):
        return super(TableBase, self).update(self.__tablename__, fields, where)

    def delete(self, where='1=0'):
        return super(TableBase, self).delete(self.__tablename__, where)

    def get(self, field='*', where='1=0'):
        return super(TableBase, self).get(self.__tablename__, field, where)

    def getlist(self, field='*', where='1=1', order='', limit=''):
        return super(TableBase, self).getlist(self.__tablename__, field, where, order, limit)


class DictTable(TableBase):
    """
    docstring for DictDB
    """
    __tablename__ = 'dicts'

    def insert(self, fields):
        # binascii.crc32 is diff between py2 and py3, the param must be bytes in py3
        import binascii
        fields.update({'uid': binascii.crc32(fields.get('name').encode('utf8')) & 0xffffffff})
        return super(DictTable, self).insert(fields, True)

    def getlist(self, field='*', where='1=1', order='ctime DESC', limit=''):
        return super(TableBase, self).getlist(self.__tablename__, field, where, order, limit)


class SentenceTable(TableBase):
    """
    docstring for SentenceTable
    """
    __tablename__ = 'sentences'

    def getlist(self, field='*', where='1=1', order='id DESC', limit=''):
        return super(TableBase, self).getlist(self.__tablename__, field, where, order, limit)


if __name__ == '__main__':
    logger.info('start debug ...')
    path = ':memory:'

    tdict = DictTable(path)
    fields = {'name': 'essensially'}
    tdict.insert(fields)
    [logger.info(row['name']) for row in tdict.getlist()]

    fields = {'name': 'renewed'}
    where = 'name="%s"' % 'essensially'
    tdict.update(fields, where)

    info = tdict.get('*', 'name="%s"' % 'renewed')
    assert info['name'] == 'renewed'

    tdict.delete('1=1')
    assert len([x for x in tdict.getlist()]) == 0

    tsentence = SentenceTable(path)
    fields = {'sentence': 'this is a sentence.'}
    tsentence.insert(fields)
    fields = {'sentence': 'this is another sentence.'}
    tsentence.insert(fields)
    [logger.info(row['sentence']) for row in tsentence.getlist()]

    tsentence.execute('DROP TABLE dicts')
    tsentence.execute('DROP TABLE sentences')
