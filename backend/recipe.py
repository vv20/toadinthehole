from common import build_response_body, create_handler
from model import Recipe


def get_recipe(event):
    if not 'queryStringParameters' in event or not 'recipeID' in event['queryStringParameters']:
        return build_response_body(400, 'Missing recipe ID')
    recipe = Recipe(event['queryStringParameters']['recipeID'])
    if not recipe.exists:
        return build_response_body(404, 'Recipe not found')
    return build_response_body(200, recipe.toJson())

def save_recipe(event):
    recipe = Recipe(event['queryStringParameters']['recipeID'], event['body'])
    recipe.save()
    return build_response_body(201, 'OK')

def delete_recipe(event):
    if not 'queryStringParameters' in event or not 'recipeID' in event['queryStringParameters']:
        return build_response_body(400, 'Missing recipe ID')
    recipe = Recipe(event['queryStringParameters']['recipeID'])
    if not recipe.exists:
        return build_response_body(404, 'Recipe not found')
    recipe.delete()
    return build_response_body(201, 'OK')

handler = create_handler({
        'GET': get_recipe,
        'POST': save_recipe,
        'DELETE': delete_recipe
})
