import django_tables2 as tables


class SearchTable(tables.Table):
    result_type = tables.Column("Result Type")
    title = tables.URLColumn(accessor="url", text=lambda x: x["title"])
    url = tables.URLColumn(verbose_name="Actions", text="View")
