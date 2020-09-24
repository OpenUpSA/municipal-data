from django.core.management.base import BaseCommand, CommandError

from municipal_finance.models import UifwexpFacts, AuditOpinionFacts

class Command(BaseCommand):
    help = 'Sample command'

    def handle(self, *args, **options):
        uifwQuery = UifwexpFacts.objects.filter(
            amount__isnull=True,
            financial_year__gt=2016,
        )
        count = 0
        for uifwItem in uifwQuery:
            auditOpinionQuery = AuditOpinionFacts.objects.filter(
                demarcation_code__exact=uifwItem.demarcation_code,
                financial_year__exact=uifwItem.financial_year,
                opinion_code__exact='unqualified',
            )
            auditOpinionCount = auditOpinionQuery.count()
            if auditOpinionCount == 1:
                opinion = auditOpinionQuery[0]
                print(opinion.demarcation_code, opinion.report_url)
                count += 1
                if count > 10: break
        # result = {}
        # uifwQuery = UifwexpFacts.objects.filter(
        #     amount__isnull=True
        # )
        # # print(uifwQuery.count())
        # for item in uifwQuery:
        #     auditQuery = AuditOpinionFacts.objects.filter(
        #         demarcation_code__exact=item.demarcation_code,
        #         financial_year__exact=item.financial_year
        #     )
        #     financial_year = str(item.financial_year)
        #     auditCount = auditQuery.count()
        #     if financial_year not in result:
        #         result[financial_year] = {}
        #     if (auditCount == 1):
        #         opinion = auditQuery[0]
        #         if opinion.opinion_label not in result[financial_year]:
        #             result[financial_year][opinion.opinion_label] = 0
        #         result[financial_year][opinion.opinion_label] += 1;
        #         # print(item.demarcation_code, item.financial_year, auditQuery[0].opinion_label)
        #     else:
        #         if 'none' not in result[financial_year]:
        #             result[financial_year]['none'] = 0
        #         result[financial_year]['none'] += 1
        #         # print(item.demarcation_code, item.financial_year, 'false')
        # print(result)
        # # self.stdout.write(self.style.SUCCESS('Sample!'))
