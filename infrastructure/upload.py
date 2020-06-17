from .models import QuarterlySpendFile

from .utils import load_excel


def process_document(id):
    """
    Get file an process it.
    """
    spend = QuarterlySpendFile.objects.get(id=id)
    try:
        path = spend.document.path
        load_excel(path, financial_year=spend.financial_year)
        spend.status = QuarterlySpendFile.SUCCESS
        spend.save()
    except Exception:
        raise ValueError("Error processing file")
        # spend_file.status = QuarterlySpendFile.SUCCESS
        # spend_file.save()
