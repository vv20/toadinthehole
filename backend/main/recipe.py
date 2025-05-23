import json

from .common import build_response_body, create_handler
from .model import Recipe


def get_recipe(event):
    if not 'queryStringParameters' in event or event['queryStringParameters'] is None or not 'recipeID' in event['queryStringParameters']:
        return build_response_body(400, 'Missing recipe ID', event)
    recipe = Recipe(slug=event['queryStringParameters']['recipeID'])
    if not recipe.exists:
        return build_response_body(404, 'Recipe not found', event)
    return build_response_body(200, recipe.toJson(), event)

def save_recipe(event):
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None and 'recipeID' in event['queryStringParameters']:
        recipe = Recipe(slug=event['queryStringParameters']['recipeID'], item=json.loads(event['body']))
    else:
        if 'body' not in event:
            return build_response_body(400, 'Missing request body', event)
        recipe = Recipe(item=json.loads(event['body']))
    recipe.save()
    return build_response_body(201, recipe.toJson(), event)

def delete_recipe(event):
    if not 'queryStringParameters' in event or not 'recipeID' in event['queryStringParameters']:
        return build_response_body(400, 'Missing recipe ID', event)
    recipe = Recipe(slug=event['queryStringParameters']['recipeID'])
    if not recipe.exists:
        return build_response_body(404, 'Recipe not found', event)
    recipe.delete()
    return build_response_body(201, 'OK', event)

handler = create_handler({
        'GET': get_recipe,
        'POST': save_recipe,
        'DELETE': delete_recipe
})
