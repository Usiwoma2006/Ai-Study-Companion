from django.core.management.base import BaseCommand
from ingestion.services.pipeline import process_document


class Command(BaseCommand):
    help = "Run the ingestion pipeline for a single document"

    def add_arguments(self, parser):
        parser.add_argument("document_id", type=int)

    def handle(self, *args, **options):
        document_id = options["document_id"]
        process_document(document_id)