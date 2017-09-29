# -*- coding: utf-8 -*-
from django.test import TestCase
from velafrica.api import utils
from velafrica.sbbtracking.models import Tracking
from rest_framework import generics


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

class Utils(TestCase):

    def setUp(self):

        pass

    def test_get_serializer_by_model(self):
        serializer = utils.get_serializer_by_model(Tracking)
        self.assertEqual(type(Tracking), type(serializer.Meta.model))

    def test_get_serializer(self):
        serializer = utils.get_serializer('sbbtracking', 'Tracking')
        self.assertEqual(type(Tracking), type(serializer.Meta.model))

    def test_get_listview_by_model(self):
        listview = utils.get_listview_by_model(Tracking)
        self.assertEqual(type(Tracking), type(listview.serializer_class.Meta.model))
        self.assertEqual(type(listview), type(generics.ListCreateAPIView))

    def test_get_listview(self):
        listview = utils.get_listview('sbbtracking', 'Tracking')
        self.assertEqual(type(Tracking), type(listview.serializer_class.Meta.model))
        self.assertEqual(type(listview), type(generics.ListCreateAPIView))

    def test_get_retrieveview_by_model(self):
        listview = utils.get_retrieveview_by_model(Tracking)
        self.assertEqual(type(Tracking), type(listview.serializer_class.Meta.model))
        self.assertEqual(type(listview), type(generics.RetrieveUpdateAPIView))

    def test_get_retrieveview(self):
        listview = utils.get_retrieveview('sbbtracking', 'Tracking')
        self.assertEqual(type(Tracking), type(listview.serializer_class.Meta.model))
        self.assertEqual(type(listview), type(generics.RetrieveUpdateAPIView))
