#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import sys
import re
import urlparse
import string
from .common import *
from .database import DictTable, SentenceTable


class GetHandler(BaseHTTPRequestHandler):
    """
    docstring for GetHandler
    """
    def do_GET(self):
        self._get_template()
        logger.info('request: %s' % self.path)
        parsed_path = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed_path.query)
        status = 200
        content = 'Page Request Failed: 404'
        try:
            ac = query.get('ac')[0]
            if ac == 'dicts':
                content = self._page_dicts()
            else:
                status = 404
        except Exception as e:
            content = self._page_index()
            logger.info('ERROR: %s' % str(e))

        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf8'))
        return

    def _get_template(self):
        with open(WEB_TEMPLATE_FILEPATH, 'rt') as f:
            template = f.read()
        self.template = template
        return template

    def _page_index(self):
        tsentence = SentenceTable()
        cur = tsentence.getlist()
        body = '\n'.join(['<li>%s</li>' % row['sentence'] for row in cur])
        body = '<ul>%s</ul>' % body

        tdict = DictTable()
        cur = tdict.getlist()
        for row in cur:
            body = re.sub(r'\b(%s)\b' % row['name'], '<i>\\1</i>', body, flags=re.IGNORECASE)

        t = string.Template(self.template)
        content = t.substitute({'body': body})
        return content

    def _page_dicts(self):
        tdict = DictTable()
        cur = tdict.getlist()
        body = '\n'.join(['<span style="padding:5px">%s</span>' % row['name'] for row in cur])
        t = string.Template(self.template)
        content = t.substitute({'body': body})
        return content


def main(port = WEB_PORT_DEFAULT):
    server = HTTPServer(('localhost', port), GetHandler)
    logger.info('Starting server %d, use <Ctrl-C> to stop' % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('server has been stoped.')
        sys.exit(1)


if __name__ == '__main__':
    main()
