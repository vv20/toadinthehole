from common import create_handler
from model import RecipeCollection


def get_recipe_collection(event):
    if 'queryStringParameters' in event and 'tags' in event['queryStringParameters']:
        collection = RecipeCollection(event['queryStringParameters']['tags'])
    else:
        collection = RecipeCollection()
    return collection

handler = create_handler({
    'GET': get_recipe_collection,
})
