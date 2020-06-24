def category_sort(queryset):
    """
    Sort the quarterly results into categories
    """
    category = {}
    if queryset:
        for result in queryset:
            category[result.indicator.category.name] = {
                "slug": result.indicator.category.slug,
                "results": [],
                "count": 0,
            }

        for result in queryset:
            category[result.indicator.category.name]["results"].append(result)
            if result.target_achived():
                category[result.indicator.category.name]["count"] += 1
    return category
