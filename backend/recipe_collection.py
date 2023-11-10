from common import build_response_body
from model import RecipeCollection

def get_recipe_collection(event):
    if not event['queryStringParameters'] or not event['queryStringParameters']['tags']:
        collection = RecipeCollection()
    else:
        collection = RecipeCollection(event['queryStringParameters']['tags'])
    return build_response_body(200, str(collections.recipes))

methodDict = {
        'GET': get_recipe_collection,
}

def handler(event, context):
    if event.httpMethod not in methodDict:
        return build_response_body(400, "HTTP method not supported")
    try:
        return methodDict[event.httpMethod](event)
    except:
        return build_response_body(500, "Internal Server Error")
