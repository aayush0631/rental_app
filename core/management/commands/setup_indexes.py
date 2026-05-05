from django.core.management.base import BaseCommand
from core.db import users_collection, services_collection, bookings_collection
import pymongo

class Command(BaseCommand):
    help = 'Setup MongoDB indexes for the Smart Services Marketplace'

    def handle(self, *args, **options):
        self.stdout.write('Setting up MongoDB indexes...')

        # Users indexes
        users_collection.create_index([("email", pymongo.ASCENDING)], unique=True)
        self.stdout.write(self.style.SUCCESS('Successfully created unique index on users.email'))

        # Services indexes
        services_collection.create_index([("location", pymongo.GEOSPHERE)])
        self.stdout.write(self.style.SUCCESS('Successfully created 2dsphere index on services.location'))
        
        services_collection.create_index([("category", pymongo.ASCENDING)])
        self.stdout.write(self.style.SUCCESS('Successfully created index on services.category'))

        services_collection.create_index([
            ("title", pymongo.TEXT),
            ("description", pymongo.TEXT)
        ])
        self.stdout.write(self.style.SUCCESS('Successfully created text index on services.title and description'))

        # Bookings indexes
        bookings_collection.create_index([("customer_id", pymongo.ASCENDING)])
        bookings_collection.create_index([("provider_id", pymongo.ASCENDING)])
        bookings_collection.create_index([("service_id", pymongo.ASCENDING)])
        self.stdout.write(self.style.SUCCESS('Successfully created indexes on bookings'))

        self.stdout.write(self.style.SUCCESS('All indexes setup successfully!'))
