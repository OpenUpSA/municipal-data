from .models import QuarterlySpendFile

from .utils import load_excel
import io


def process_document(id):
    """
    Get file an process it.
    """
    spend = QuarterlySpendFile.objects.get(id=id)
    try:
        file_contents = spend.document.read()
        load_excel("", financial_year=spend.financial_year, file_contents=file_contents)
        spend.status = QuarterlySpendFile.SUCCESS
        spend.save()
    except Exception:
        spend.status = QuarterlySpendFile.ERROR
        spend.save()
        raise ValueError("Error processing file")
