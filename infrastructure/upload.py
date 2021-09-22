from .models import QuarterlySpendFile, AnnualSpendFile

from .utils import load_excel
import io


def process_annual_document(id):
    """
    Get file and process it.
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
        raise ValueError("Error processing annual spend file")

def process_quarterly_document(id):
    """
    Get file and process it.
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
        raise ValueError("Error processing quarterly spend file")
