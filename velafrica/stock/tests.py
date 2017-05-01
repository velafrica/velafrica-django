# -*- coding: utf-8 -*-
from django.test import TestCase

from velafrica.organisation.models import Country
from velafrica.stock.models import *


class StockTransferBookingTest(TestCase):
    def setUp(self):
        c = Category.objects.create(name="Reifen und Schläuche")
        p1 = Product.objects.create(articlenr="100.100", name="Reifen 24''", hscode="0", category=c, sales_price=12.0)
        p2 = Product.objects.create(articlenr="100.102", name="Reifen 26''", hscode="0", category=c, sales_price=14.0)
        p3 = Product.objects.create(articlenr="100.104", name="Reifen 28''", hscode="0", category=c, sales_price=16.0)

        country = Country.objects.create(name="Schweiz")
        a = Address.objects.create(country=country)
        o = Organisation.objects.create(name="Velafrica")
        w1 = Warehouse.objects.create(name="Ersatzteillager", organisation=o, stock_management=True)
        w2 = Warehouse.objects.create(name="Exportlager", organisation=o, stock_management=False)

        Stock.objects.create(product=p1, warehouse=w1, amount=20)
        Stock.objects.create(product=p2, warehouse=w1, amount=20)
        Stock.objects.create(product=p3, warehouse=w1, amount=20)

        sl = StockList.objects.create()

        StockListPosition.objects.create(product=p1, amount=10, stocklist=sl)
        StockListPosition.objects.create(product=p2, amount=8, stocklist=sl)
        StockListPosition.objects.create(product=p3, amount=6, stocklist=sl)


    def test_stocktransfer_book_and_revoke_incoming(self):
        """
        Test if the stock adjustments are made correctly when booking and revoking a Stock Transfer.
        """
        w1 = Warehouse.objects.get(name="Ersatzteillager")
        w2 = Warehouse.objects.get(name="Exportlager")
        sl = StockList.objects.first()
        st = StockTransfer.objects.create(warehouse_from=w2, warehouse_to=w1, stocklist=sl)

        p1 = Product.objects.get(articlenr="100.100")
        p2 = Product.objects.get(articlenr="100.102")
        p3 = Product.objects.get(articlenr="100.104")

        s1 = Stock.objects.get(product=p1, warehouse=w1)
        s2 = Stock.objects.get(product=p2, warehouse=w1)
        s3 = Stock.objects.get(product=p3, warehouse=w1)

        self.assertEqual(20, s1.amount)
        self.assertEqual(20, s2.amount)
        self.assertEqual(20, s3.amount)

        st.book()

        s1.refresh_from_db()
        s2.refresh_from_db()
        s3.refresh_from_db()
        st.refresh_from_db()
        sts = StockChange.objects.filter(stocktransfer=st)

        self.assertEqual(30, s1.amount)
        self.assertEqual(28, s2.amount)
        self.assertEqual(26, s3.amount)
        self.assertTrue(st.booked)
        self.assertEqual(2, sts.count())

        st.revoke()

        s1.refresh_from_db()
        s2.refresh_from_db()
        s3.refresh_from_db()
        st.refresh_from_db()
        sts = StockChange.objects.filter(stocktransfer=st)

        self.assertEqual(20, s1.amount)
        self.assertEqual(20, s2.amount)
        self.assertEqual(20, s3.amount)
        self.assertFalse(st.booked)
        self.assertEqual(0, sts.count())

    def test_stocktransfer_book_outgoing(self):
        """
        Test if the stock adjustments are made correctly when booking and revoking a Stock Transfer.
        """
        w1 = Warehouse.objects.get(name="Ersatzteillager")
        w2 = Warehouse.objects.get(name="Exportlager")
        sl = StockList.objects.first()
        st = StockTransfer.objects.create(warehouse_from=w1, warehouse_to=w2, stocklist=sl)

        p1 = Product.objects.get(articlenr="100.100")
        p2 = Product.objects.get(articlenr="100.102")
        p3 = Product.objects.get(articlenr="100.104")

        s1 = Stock.objects.get(product=p1)
        s2 = Stock.objects.get(product=p2)
        s3 = Stock.objects.get(product=p3)

        self.assertEqual(20, s1.amount)
        self.assertEqual(20, s2.amount)
        self.assertEqual(20, s3.amount)

        st.book()
        s1.refresh_from_db()
        s2.refresh_from_db()
        s3.refresh_from_db()
        st.refresh_from_db()
        sts = StockChange.objects.filter(stocktransfer=st)

        self.assertEqual(10, s1.amount)
        self.assertEqual(12, s2.amount)
        self.assertEqual(14, s3.amount)
        self.assertTrue(st.booked)
        self.assertEqual(2, sts.count())

        st.revoke()

        s1.refresh_from_db()
        s2.refresh_from_db()
        s3.refresh_from_db()
        st.refresh_from_db()
        sts = StockChange.objects.filter(stocktransfer=st)

        self.assertEqual(20, s1.amount)
        self.assertEqual(20, s2.amount)
        self.assertEqual(20, s3.amount)
        self.assertFalse(st.booked)
        self.assertEqual(0, sts.count())

    def test_stocktransfer_fake_book_incoming(self):
        """
        Test if stocks stay untouched when making a fake booking of a Stock Transfer.
        """
        w1 = Warehouse.objects.get(name="Ersatzteillager")
        w2 = Warehouse.objects.get(name="Exportlager")
        sl = StockList.objects.first()
        st = StockTransfer.objects.create(warehouse_from=w2, warehouse_to=w1, stocklist=sl)

        p1 = Product.objects.get(articlenr="100.100")
        p2 = Product.objects.get(articlenr="100.102")
        p3 = Product.objects.get(articlenr="100.104")

        s1 = Stock.objects.get(product=p1, warehouse=w1)
        s2 = Stock.objects.get(product=p2, warehouse=w1)
        s3 = Stock.objects.get(product=p3, warehouse=w1)

        self.assertEqual(20, s1.amount)
        self.assertEqual(20, s2.amount)
        self.assertEqual(20, s3.amount)

        st.book(fake=True)

        s1.refresh_from_db()
        s2.refresh_from_db()
        s3.refresh_from_db()
        st.refresh_from_db()
        sts = StockChange.objects.filter(stocktransfer=st)

        self.assertEqual(20, s1.amount)
        self.assertEqual(20, s2.amount)
        self.assertEqual(20, s3.amount)
        self.assertTrue(st.booked)
        self.assertEqual(2, sts.count())

        st.revoke()

        s1.refresh_from_db()
        s2.refresh_from_db()
        s3.refresh_from_db()
        st.refresh_from_db()
        sts = StockChange.objects.filter(stocktransfer=st)

        self.assertEqual(20, s1.amount)
        self.assertEqual(20, s2.amount)
        self.assertEqual(20, s3.amount)
        self.assertFalse(st.booked)
        self.assertEqual(0, sts.count())