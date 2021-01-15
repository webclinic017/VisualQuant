import logging
import dash_html_components as html


class List:

    def __init__(self, column_count: int, column_width: int = 50):
        self.logger = logging.getLogger(__name__)
        self.column_count = column_count
        self.column_width = column_width
        self.entries = {}

    def add_entry(self, name: str, value):
        self.entries[name] = value

    def children_html(self):
        html_l = []
        for child in self.entries:
            html_l.append(html.Td(f"{child}{str(self.entries[child]).rjust(self.column_width)}"))
        return html_l

    def get_html(self):
        html_list = html.Tr(children=self.children_html())
        return html_list
