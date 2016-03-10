# vim: sw=4:sts=4

from pkg_resources import resource_filename

from genshi.builder import tag

from trac.core import Component, implements
from trac.util.compat import *
from trac.web.api import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet

from trac.cache import cached

from trac.ticket.model import Type, Milestone
from trac.util.translation import _


class TracHierchicalMainNav (Component):

    implements(IRequestFilter, ITemplateProvider)

    ## ITemplateProvider methods
    def get_htdocs_dirs (self):
        yield 'mainnavsubmenu', resource_filename(__name__, 'htdocs')
    def get_templates_dirs (self):
        return []

    ## IRequestFilter methods
    def post_process_request (self, req, template, data, content_type):
	add_stylesheet(req, 'mainnavsubmenu/css/menu.css')
        mainnav = req.chrome['nav']['mainnav']

        for item in mainnav:
            submenus = self._submenus.get(item['name'])
            if not submenus:
                continue

            ul = tag.ul()
            for _item in submenus:
                href = _item.get('href')
                if href == '@milestones@':
                    self._add_milestones(req, ul)
                elif href == '@ticket_types@':
                    self._add_ticket_types(req, ul)
                elif href == '@saved_query@':
                    self._add_saved_query(req, ul, _item.get('label'))
                else:
                    label = _item.get('label') or _item.get('name')
                    self._add_item(req, ul, label, href)

            item['label'] = tag(item['label'], ul)

        return (template, data, content_type)

    def pre_process_request (self, req, handler):
        return handler

    def _add_item (self, req, ul, label, href, expand_href=True):
        if href and expand_href and href.startswith('/'):
            href = req.href + href
        ul(tag.li(tag.a(_(label), href=href)))

    def _add_milestones (self, req, ul):
        for milestone in Milestone.select(self.env, False):
            label = milestone.name
            href = '/milestone/' + label
            self._add_item(req, ul, label, href)

    def _add_ticket_types (self, req, ul):
        for t in Type.select(self.env):
            label = t.name
            href = '/newticket?type=' + label
            self._add_item(req, ul, label, href, False)

    def _add_saved_query (self, req, ul, label):
        query_href = req.session.get('query_href')
        if query_href:
            self._add_item(req, ul, label or 'Last Query', query_href)

    @cached
    def _submenus (self):
        submenus = {}
        section = self.env.config['mainnav']
        for k, options in groupby(section, lambda k: k.split('.')[0]):
            smenus = submenus.setdefault(k, {})
            for opt in options:
                elts = opt.split('.')
                if len(elts) < 3:
                    continue
                name = elts[1]
                menu = smenus.setdefault(name, {'name': name})
                menu[elts[2]] = section.get(opt)

        # sort and make canonical
        for key,v in submenus.items():
            order = section.get(key+'.order')
            if order:
                v = [v[k.strip()] for k in order.split(',')]
            else:
                v = v.values()
            submenus[key] = v
        return submenus
