# -*- coding: utf-8 -*-
from django.test import TestCase

from velafrica.api import utils


class UrlResolver(TestCase):
    def setUp(self):
        pass

    def url_pattern_names(self):
        # TODO: write appropriate test, somehow mock urls?
        # response = utils.load_url_pattern_names("", [])
        self.assertEqual(True, True)

    def api_root_listing(self):
        # TODO: write appropriate test, somehow mock urls?
        # response = utils.get_api_root_listing_from_urls([], "json")
        self.assertEqual(True, True)
