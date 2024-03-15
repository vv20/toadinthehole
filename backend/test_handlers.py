import json
import os

import pytest
from image import handler as image_handler
from recipe import handler as recipe_handler
from recipe_collection import handler as recipe_collection_handler
from test_util import InMemoryDatabaseTable

RECIPES_TABLE = InMemoryDatabaseTable()


@pytest.fixture
def data_setup(mocker):
    os.environ['ALLOWED_ORIGINS'] = 'http://localhost:3000'
    os.environ['IMAGE_BUCKET_ARN'] = 'image_bucket_arn'
    os.environ['RECIPE_TABLE_NAME'] = 'recipe_table_name'

    mock_dynamodb = mocker.patch('model.dynamodb')
    mock_recipe_table = mock_dynamodb.Table.return_value
    RECIPES_TABLE.bind_to_mock(mock_recipe_table)
    RECIPES_TABLE.setup('backend/test-assets/setup-data.json')

    mock_s3 = mocker.patch('image.s3')
    mock_s3.generate_presigned_url.return_value = 'https://presigned.url'


@pytest.mark.parametrize(
        'resource,scenario,expected_data_after_file_name',
        [

            ('/collection', 'get-all-recipes', 'setup-data.json'),
            ('/collection', 'get-recipes-with-tag1', 'setup-data.json'),
            ('/collection', 'get-recipes-with-tag1-and-tag2', 'setup-data.json'),
            ('/collection', 'get-recipes-with-non-existent-tag', 'setup-data.json'),
            ('/recipe', 'get-recipe1', 'setup-data.json'),
            ('/recipe', 'get-non-existent-recipe', 'setup-data.json'),
            ('/recipe', 'edit-recipe', 'data-with-edited-recipe.json'),
            ('/recipe', 'create-new-recipe', 'data-with-new-recipe.json'),
            ('/recipe', 'create-new-recipe-without-body', 'setup-data.json'),
            ('/recipe', 'delete-recipe', 'data-with-deleted-recipe.json'),
            ('/recipe', 'delete-non-existent-recipe', 'setup-data.json'),
            ('/image', 'get-presigned-url', 'setup-data.json')

        ]
    )
def test_handlers(
        data_setup,
        resource,
        scenario,
        expected_data_after_file_name):
    request = {}
    with open('backend/test-assets/' + scenario + '-request.json', 'r') as request_file:
        request = json.load(request_file)

    expected_response = {}
    with open('backend/test-assets/' + scenario + '-response.json', 'r') as response_file:
        expected_response = json.load(response_file)

    actual_response = {
            '/collection': recipe_collection_handler,
            '/image': image_handler,
            '/recipe': recipe_handler
    }[resource](request, {})

    assert actual_response == expected_response

    if expected_data_after_file_name is not None:
        with open('backend/test-assets/' + expected_data_after_file_name, 'r') as expected_data_after_file:
            expected_data_after = json.load(expected_data_after_file)
            assert RECIPES_TABLE.rows == expected_data_after
