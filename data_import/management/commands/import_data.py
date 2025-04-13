# data_import/management/commands/import_data.py
from django.core.management.base import BaseCommand
import pandas as pd
from data_import.models import ExcelImport
from repairing_service.models import ServiceCategory, Service
from decimal import Decimal

class Command(BaseCommand):
    help = 'Imports data from Excel file and adds it to the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.stdout.write(f"Importing data from {file_path}")

        # Save the file as an ExcelImport object
        import_file = ExcelImport(file=file_path)
        import_file.save()

        # Read the Excel file using pandas
        try:
            df = pd.read_excel(file_path)

            # Iterate through the rows and create instances
            for _, row in df.iterrows():
                category_name = row['Category']
                service_name = row['Name']
                base_price = Decimal(row['Base Price'])
                discount = Decimal(row['Discount'])
                description = row['Description']
                duration = row['Duration']
                warranty = row['Warranty']
                recommended = row['Recommended']

                # Get or create the ServiceCategory
                category, created = ServiceCategory.objects.get_or_create(name=category_name)

                # Create the Service object
                Service.objects.create(
                    name=service_name,
                    category=category,
                    base_price=base_price,
                    discount=discount,
                    description=description,
                    duration=duration,
                    warranty=warranty,
                    recommended=recommended
                )

            self.stdout.write(self.style.SUCCESS('Data imported successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
