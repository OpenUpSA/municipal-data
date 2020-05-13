def category_sort(queryset):
    """
    Sort the quarterly results in to categories
    """
    category = {}
    if queryset:
        for result in queryset:
            category[result.indicator.category.name] = {
                "slug": result.indicator.category.slug,
                "results": [],
            }

        for result in queryset:
            category[result.indicator.category.name]["results"].append(result)
    return category
