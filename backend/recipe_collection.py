from common import build_response_body
from model import RecipeCollection

def get_recipe_collection(event):
    if 'queryStringParameters' in event and 'tags' in event['queryStringParameters']:
        collection = RecipeCollection(event['queryStringParameters']['tags'])
    else:
        collection = RecipeCollection()
    return build_response_body(200, str(collection.recipes))

methodDict = {
        'GET': get_recipe_collection,
}

def handler(event, context):
    if event['httpMethod'] not in methodDict:
        return build_response_body(400, "HTTP method not supported")
    try:
        return methodDict[event['httpMethod']](event)
    except:
        return build_response_body(500, "Internal Server Error")
