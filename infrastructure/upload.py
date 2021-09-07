from .models import QuarterlySpendFile, AnnualSpendFile

from .utils import load_excel
import io


def process_document(id):
    """
    Get file an process it.
    """
    spend = AnnualSpendFile.objects.get(id=id)

    try:
        file_contents = spend.document.read()
        load_excel("", financial_year=spend.financial_year, file_contents=file_contents)
        spend.status = AnnualSpendFile.SUCCESS
        spend.save()
    except Exception:
        spend.status = AnnualSpendFile.ERROR
        spend.save()
        raise ValueError("Error processing file")
