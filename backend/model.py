import json
import os

import boto3
from boto3.dynamodb.conditions import Attr, Or
from slugify import slugify

dynamodb = boto3.resource('dynamodb')

class Recipe:
    def __init__(self, slug=None, item=None):
        self.table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])
        self.slug = slug
        self.exists = False
        if slug is None and item is not None and 'name' in item:
            self.slug = slugify(item['name'])

        # try to fetch the recipe from the database
        queryResponse = self.table.get_item(
            Key = {
                'slug': slug
            }
        )
        if 'Item' in queryResponse:
            self.exists = True
            self.name = queryResponse['Item']['name']
            self.description = queryResponse['Item']['description']
            self.image_id = queryResponse['Item']['image_id']
            self.tags = queryResponse['Item']['tags']

        # override remote attributes with local ones
        if item is not None:
            self.name = item['name']
            self.description = item['description']
            self.image_id = item['image_id']
            self.tags = item['tags']

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
                        'slug': self.slug
                    },
                    UpdateExpression='SET name=:name, description=:description, image_id=:image_id, tags=:tags',
                    ExpressionAttributeValues={
                        ':name': self.name,
                        ':description': self.description,
                        ':image_id': self.image_id,
                        ':tags': self.tags
                    })
        else:
            self.table.put_item(
                    Item={
                        'slug': self.slug,
                        'name': self.name,
                        'description': self.description,
                        'image_id': self.image_id,
                        'tags': self.tags
                    })

    def delete(self):
        if not self.exists:
            return
        self.table.delete_items(
                Key={
                    'slug': self.slug
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
                    condition = Attr('tags').contains(tag)
                else:
                    condition = Or(condition, Attr('tags').contains(tag))
            queryResult = self.table.scan(FilterExpression=condition)
        else:
            queryResult = self.table.scan()
        self.recipes = [Recipe(item['slug'], item) for item in queryResult['Items']]
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
