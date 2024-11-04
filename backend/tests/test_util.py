import json


class InMemoryDatabaseTable:

    def __init__(self):
        self.rows = []

    def setup(self, setup_data_file_name):
        with open(setup_data_file_name, 'r') as setup_data_file:
            self.rows = json.load(setup_data_file)

    def bind_to_mock(self, mock_table):
        mock_table.scan.side_effect = self.scan
        mock_table.get_item.side_effect = self.get_item
        mock_table.update_item.side_effect = self.update_item
        mock_table.put_item.side_effect = self.put_item
        mock_table.delete_item.side_effect = self.delete_items

    def scan(self, *args, **kwargs):
        result = self.rows
        if 'FilterExpression' in kwargs:
            filter_expression = kwargs['FilterExpression']
            result = [row for row in result if _evaluate_filter(row, filter_expression)]
        return {
                'Items': result
        }

    def get_item(self, *args, **kwargs):
        possible_results = [row for row in self.rows if _row_matches_key(row, kwargs['Key'])]
        if len(possible_results) > 0:
            return {
                'Item': possible_results[0]
            }
        return {}

    def update_item(self, *args, **kwargs):
        item_index = -1
        for i in range(len(self.rows)):
            if _row_matches_key(self.rows[i], kwargs['Key']):
                item_index = i
                break
        if item_index == -1:
            return
        for attribute_name in kwargs['ExpressionAttributeValues']:
            self.rows[i]['recipe_' + attribute_name.replace(':', '')] = kwargs['ExpressionAttributeValues'][attribute_name]

    def delete_items(self, *args, **kwargs):
        self.rows = [row for row in self.rows if not _row_matches_key(row, kwargs['Key'])]

    def put_item(self, *args, **kwargs):
        self.rows.append(kwargs['Item'])


def _row_matches_key(row, keyset):
    return any([True for key in keyset if row[key] == keyset[key]])

def _evaluate_filter(row, filter_expression):
    return {
            'OR': _evaluate_or_filter,
            'contains': _evaluate_contains_filter
    }[filter_expression.get_expression()['operator']](row, filter_expression.get_expression()['values'])

def _evaluate_or_filter(row, values):
    return _evaluate_filter(row, values[0]) or _evaluate_filter(row, values[1])

def _evaluate_contains_filter(row, values):
    return values[1] in row[values[0].name]
