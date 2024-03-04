import json
import os

import pytest
from recipe_collection import handler as recipe_collection_handler


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

    def _evaluate_filter(self, row, filter_expression):
        return {
                'OR': self._evaluate_or_filter,
                'contains': self._evaluate_contains_filter
        }[filter_expression.get_expression()['operator']](row, filter_expression.get_expression()['values'])

    def _evaluate_or_filter(self, row, values):
        return self._evaluate_filter(row, values[0]) or self._evaluate_filter(row, values[1])

    def _evaluate_contains_filter(self, row, values):
        return values[1] in row[values[0].name]


RECIPES_TABLE = InMemoryDatabaseTable()


@pytest.fixture
def data_setup(mocker):
    os.environ['RECIPE_TABLE_NAME'] = 'recipe_table_name'

    RECIPES_TABLE.setup('backend/test-assets/setup_data.json')

    mock_dynamodb = mocker.patch('model.dynamodb')
    mock_recipe_table = mock_dynamodb.Table.return_value

    mock_recipe_table.scan.side_effect = RECIPES_TABLE.scan


@pytest.mark.parametrize(
        'http_method,resource,query_parameters_file_name,response_code,expected_response_body_file_name,expected_data_after_file_name',
        [
            ('GET','/collection',None,200,'all_recipes.json','setup_data.json'),
            ('GET','/collection','tag1-search.json',200,'tag1-recipes.json','setup_data.json'),
            ('GET','/collection','tag1-and-tag2-search.json',200,'tag1-and-tag2-recipes.json','setup_data.json')
        ]
    )
def test_handlers(
        data_setup,
        http_method,
        resource,
        query_parameters_file_name,
        response_code,
        expected_response_body_file_name,
        expected_data_after_file_name):
    # set up the event to be injected
    event = {
            'httpMethod': http_method
    }
    if query_parameters_file_name is not None:
        with open('backend/test-assets/' + query_parameters_file_name, 'r') as query_parameters_file:
            event['queryStringParameters'] = json.load(query_parameters_file)

    # choose the handler
    handler = {
            '/collection': recipe_collection_handler
    }[resource]

    # run the test
    response = handler(event, {})

    # assert the result
    assert response['statusCode'] == response_code
    if expected_response_body_file_name is not None:
        with open('backend/test-assets/' + expected_response_body_file_name, 'r') as expected_response_body_file:
            expected_response_body = json.load(expected_response_body_file)
            assert json.loads(response['body']) == expected_response_body
    if expected_data_after_file_name is not None:
        with open('backend/test-assets/' + expected_data_after_file_name, 'r') as expected_data_after_file:
            expected_data_after = json.load(expected_data_after_file)
            assert RECIPES_TABLE.scan()['Items'] == expected_data_after
