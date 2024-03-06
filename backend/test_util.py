import json


class InMemoryDatabaseTable:

    def __init__(self):
        self.rows = []

    def setup(self, filename):
        with open(filename, 'r') as setup_data_file:
            self.rows = json.load(setup_data_file)

    def scan(self, *args, **kwargs):
        result = self.rows
        if 'FilterExpression' in kwargs:
            filter_expression = kwargs['FilterExpression']
            result = [row for row in result if self._evaluate_filter(row, filter_expression)]
        return {
                'Items': result
        }

    def get_item(self, *args, **kwargs):
        possible_results = [row for row in self.rows if self._row_matches_key(row, kwargs['Key'])]
        if len(possible_results) > 0:
            return {
                'Item': possible_results[0]
            }
        return {}

    def update_item(self, *args, **kwargs):
        item_index = -1
        for i in range(len(self.rows)):
            if self._row_matches_key(self.rows[i], kwargs['Key']):
                item_index = i
                break
        if item_index == -1:
            return
        for attribute_name in kwargs['ExpressionAttributeValues']:
            self.rows[i][attribute_name.replace(':', '')] = kwargs['ExpressionAttributeValues'][attribute_name]

    def delete_items(self, *args, **kwargs):
        self.rows = [row for row in self.rows if not self._row_matches_key(row, kwargs['Key'])]

    def put_item(self, *args, **kwargs):
        self.rows.append(kwargs['Item'])

    def _row_matches_key(self, row, keyset):
        return any([True for key in keyset if row[key] == keyset[key]])

    def _evaluate_filter(self, row, filter_expression):
        return {
                'OR': self._evaluate_or_filter,
                'contains': self._evaluate_contains_filter
        }[filter_expression.get_expression()['operator']](row, filter_expression.get_expression()['values'])

    def _evaluate_or_filter(self, row, values):
        return self._evaluate_filter(row, values[0]) or self._evaluate_filter(row, values[1])

    def _evaluate_contains_filter(self, row, values):
        return values[1] in row[values[0].name]
