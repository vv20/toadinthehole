from common import build_response_body
from model import Recipe

def get_recipe(event):
    if not event['queryStringParameters'] or not event['queryStringParameters']['recipe']:
        return build_response_body(400, 'Missing recipe ID')
    recipe = Recipe(event['queryStringParameters']['recipe'])
    if not recipe.exists:
        return build_response_body(404, 'Recipe not found')
    return build_response_body(200, str(recipe))

def save_recipe(event):
    recipe = Recipe(event['queryStringParameters']['recipe'])
    recipe.save()
    return build_response_body(201, 'OK')

def delete_recipe(event):
    if not event['queryStringParameters'] or not event['queryStringParameters']['recipe']:
        return build_response_body(400, 'Missing recipe ID')
    recipe = Recipe(event['queryStringParameters']['recipe'])
    if not recipe.exists:
        return build_response_body(404, 'Recipe not found')
    recipe.delete()
    return build_response_body(201, 'OK')

methodDict = {
        'GET': get_recipe,
        'POST': save_recipe,
        'DELETE': delete_recipe
}

def handler(event, context):
    if event['httpMethod'] not in methodDict:
        return build_response_body(400, "HTTP method not supported")
    try:
        return methodDict[event.httpMethod](event)
    except:
        return build_response_body(500, "Internal Server Error")
