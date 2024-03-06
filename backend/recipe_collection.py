from common import build_response_body, create_handler
from model import RecipeCollection


def get_recipe_collection(event):
    if 'queryStringParameters' in event and 'tags' in event['queryStringParameters']:
        collection = RecipeCollection(event['queryStringParameters']['tags'])
    else:
        collection = RecipeCollection()
    return build_response_body(200, collection.toJson())

handler = create_handler({
    'GET': get_recipe_collection,
})
