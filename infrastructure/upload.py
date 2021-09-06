from .models import QuarterlySpendFile, AnnualSpendFile

from .utils import load_excel
import io


def process_document(id, file_type):
    """
    Get file an process it.
    """
    if file_type == "annual":
        spend = AnnualSpendFile.objects.get(id=id)
    else:
        spend = QuarterlySpendFile.objects.get(id=id)

    try:
        file_contents = spend.document.read()
        load_excel("", financial_year=spend.financial_year, file_contents=file_contents)
        spend.status = spend.SUCCESS
        spend.save()
    except Exception:
        spend.status = spend.ERROR
        spend.save()
        raise ValueError("Error processing file")
