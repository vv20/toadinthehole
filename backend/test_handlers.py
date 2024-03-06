import json
import os

import pytest
from recipe_collection import handler as recipe_collection_handler
from recipe import handler as recipe_handler


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
        possible_results = self.rows
        for key in kwargs['Key']:
            possible_results = [row for row in possible_results if row[key] == kwargs['Key'][key]]
        if len(possible_results) > 0:
            return {
                'Item': possible_results[0]
            }
        return {}

    def update_item(self, *args, **kwargs):
        item_index = -1
        for i in range(len(self.rows)):
            item_matches = all([True for key in kwargs['Key'] if self.rows[i] == kwargs['Key'][key]])
            if item_matches:
                item_index = i
                break
        if item_index == -1:
            return
        for attribute_name in kwargs['ExpressionAttributeValues']:
            self.rows[i][attribute_name.replace(':', '')] = kwargs['ExpressionAttributeValues'][attribute_name]

    def put_item(self, *args, **kwargs):
        self.rows.append(kwargs['Item'])

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

    RECIPES_TABLE.setup('backend/test-assets/setup-data.json')

    mock_dynamodb = mocker.patch('model.dynamodb')
    mock_recipe_table = mock_dynamodb.Table.return_value

    mock_recipe_table.scan.side_effect = RECIPES_TABLE.scan
    mock_recipe_table.get_item.side_effect = RECIPES_TABLE.get_item
    mock_recipe_table.update_item.side_effect = RECIPES_TABLE.update_item
    mock_recipe_table.put_item.side_effect = RECIPES_TABLE.put_item


@pytest.mark.parametrize(
        'http_method,resource,query_parameters_file_name,request_body_file_name,response_code,expected_response_body_file_name,expected_data_after_file_name',
        [
            ('GET', '/collection', None, None, 200, 'all-recipes.json', 'setup-data.json'), # get all recipes
            ('GET','/collection', 'tag1-search.json', None, 200, 'tag1-recipes.json', 'setup-data.json'), # get all recipes with tag1
            ('GET','/collection', 'tag1-and-tag2-search.json', None, 200, 'tag1-and-tag2-recipes.json', 'setup-data.json'), # get all recipes with tags 1 and 2
            ('GET', '/recipe', 'recipe1-search.json', None, 200, 'recipe1.json', 'setup-data.json'), # get recipe1
            ('POST', '/recipe', 'recipe1-search.json', 'recipe1-edited.json', 201, None, 'data-with-edited-recipe.json'), # edit recipe1
            ('POST', '/recipe', None, 'recipe5.json', 201, None, 'data-with-new-recipe.json') # create new recipe
        ]
    )
def test_handlers(
        data_setup,
        http_method,
        resource,
        query_parameters_file_name,
        request_body_file_name,
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

    if request_body_file_name is not None:
        with open('backend/test-assets/' + request_body_file_name, 'r') as request_body_file:
            event['body'] = json.load(request_body_file)

    # choose the handler
    handler = {
            '/collection': recipe_collection_handler,
            '/recipe': recipe_handler
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
            assert RECIPES_TABLE.rows == expected_data_after
