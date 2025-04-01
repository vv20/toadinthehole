import json
import os

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, Or
from slugify import slugify

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

class Recipe:
    def __init__(self, slug=None, item=None):
        print('Recipe: ' + str(item))
        self.table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])
        self.slug = slug
        self.exists = False
        if slug is None and item is not None and 'name' in item:
            self.slug = slugify(item['name'])

        # try to fetch the recipe from the database
        queryResponse = self.table.get_item(
            Key = {
                'recipe_slug': self.slug
            }
        )
        stored_item = {}
        if 'Item' in queryResponse:
            self.exists = True
            stored_item = queryResponse['Item']
        received_item = {}
        if item is not None:
            received_item = item

        self.name = get_attribute(stored_item, received_item, 'name', default='')
        self.description = get_attribute(stored_item, received_item, 'description', default='')
        self.image_id = get_attribute(stored_item, received_item, 'image_id', default=None)
        self.tags = get_attribute(stored_item, received_item, 'tags', default=[])

    def toDict(self):
        return {
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'image_id': self.image_id,
            'tags': self.tags
        }

    def toJson(self):
        return json.dumps(self.toDict())

    def save(self):
        if self.exists:
            self.table.update_item(
                    Key={
                        'recipe_slug': self.slug
                    },
                    UpdateExpression='SET recipe_name=:name, recipe_description=:description, recipe_image_id=:image_id, recipe_tags=:tags',
                    ExpressionAttributeValues={
                        ':name': self.name,
                        ':description': self.description,
                        ':image_id': self.image_id,
                        ':tags': self.tags
                    })
        else:
            self.table.put_item(
                    Item={
                        'recipe_slug': self.slug,
                        'recipe_name': self.name,
                        'recipe_description': self.description,
                        'recipe_image_id': self.image_id,
                        'recipe_tags': self.tags
                    })

    def delete(self):
        if not self.exists:
            return
        if self.image_id:
            try:
                s3.delete_object(
                    Bucket=os.environ['IMAGE_BUCKET_NAME'],
                    Key='/public/' + self.image_id + '.jpg')
            except ClientError:
                pass
        self.table.delete_item(
                Key={
                    'recipe_slug': self.slug
                })
        self.exists = False


class RecipeCollection:
    def __init__(self, tags=[]):
        self.table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])
        condition = None
        queryResult = None
        if len(tags) > 0:
            self.tags = tags
            for tag in tags:
                if condition is None:
                    condition = Attr('recipe_tags').contains(tag)
                else:
                    condition = Or(condition, Attr('recipe_tags').contains(tag))
            queryResult = self.table.scan(FilterExpression=condition)
        else:
            queryResult = self.table.scan()
        self.recipes = [Recipe(item['recipe_slug'], item) for item in queryResult['Items']]
        # collect the tags from all collected recipes
        self.tags = set()
        for recipe in self.recipes:
            for tag in recipe.tags:
                self.tags.add(tag)

    def toJson(self):
        return json.dumps({
            'recipes': [r.toDict() for r in self.recipes],
            'tags': sorted(list(self.tags))
        })

def get_attribute(stored_item, received_item, attribute_name, default=None):
    result = default
    if 'recipe_' + attribute_name in stored_item:
        result = stored_item['recipe_' + attribute_name]
    if attribute_name in received_item:
        result = received_item[attribute_name]
    return result