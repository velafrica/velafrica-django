# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from velafrica.organisation.models import Address, Country
from velafrica.collection.models import Dropoff
from django.db.models import Q
import csv

class Command(BaseCommand):
    help = 'meep'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+')

    def handle(self, *args, **options):
        header = {
            0: 'Firma',
            1: 'Anrede',
            2: 'Vorname',
            3: 'Nachname',
            4: 'Strasse',
            5: 'PLZ',
            6: 'Ort',
            7: 'Öffnungszeiten',
            8: 'Telefon',
            9: 'Pin Farbe',
            10: 'Temporär',
            11: 'Transporte'
        }

        with open(options['path'][0], 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            country = Country.objects.get(name='Schweiz')
            firstline = True
            sbb_checks = [
                '<a target="_blank" href="http://velafrica.ch.darwin.sui-inter.net/de/Kontakt/Kontaktformular">velafrica.ch</a>'.decode('utf-8'),
                '<a target="_blank" href="http://www.velosfuerafrika.ch/vfa/kontakt/kontakt.html">velosfuerafrika.ch</a>'.decode('utf-8'),
                '<a target="_blank" href="http://velafrica.ch.darwin.sui-inter.net/fr/Contact/Formulaire-de-contact">velafrica.ch</a>'.decode('utf-8')
            ]

            for row in reader:
                if firstline:
                    firstline = False
                    continue

                print('------------------ start')

                index = 0
                csv_item = {}
                for value in row:
                    csv_item.update({header[index]: value.decode('utf-8')})
                    index += 1

                q = Q(street=csv_item['Strasse']) & Q(zipcode=csv_item['PLZ']) & Q(city=csv_item['Ort'])
                address = Address.objects.filter(q)
                address_count = address.count()
                address_id = -1
                if address_count == 0:
                    new_address = Address(
                        street=csv_item['Strasse'],
                        zipcode=csv_item['PLZ'],
                        city=csv_item['Ort'],
                        country=country)
                    new_address.save()
                    new_address.get_geolocation()
                    print(u'address created: {} with id {}'.format(new_address, new_address.pk))
                    address_id = new_address.pk
                else:
                    print(u'address known: {}'.format(address.first()))
                    address_id = address.first().pk

                new_dropoff = Dropoff(
                    active=True,
                    address_id=address_id,
                    contact_person=u'{} {} {}'.format(csv_item['Anrede'], csv_item['Vorname'], csv_item['Nachname']),
                    phone_number=csv_item['Telefon'],
                    opening_time=csv_item['Öffnungszeiten']
                )

                if csv_item['Firma']:
                    new_dropoff.name = csv_item['Firma']
                else:
                    new_dropoff.name = 'Unbenannt'


                for sbb_check in sbb_checks:
                    if sbb_check in csv_item['Öffnungszeiten']:
                        new_dropoff.sbb = True

                if not new_dropoff.sbb:
                    new_dropoff.pickup = True

                new_dropoff.save()
                print(u'successfully imported {}'.format(new_dropoff))

                print('------------------ end')

