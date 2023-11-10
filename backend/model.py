import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')

class Recipe:
    def __new__(self, slug, item=None):
        self.table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])
        self.slug = slug
        self.item = None
        if not item:
            queryResponse = self.table.get_item(
                    Key = {
                        'slug': slug
                    }
            )
            if 'item' in queryResponse:
                self.item = queryResponse['item']
        else:
            self.item = item
        if self.item:
            self.name = queryResponse['item']['name']
            self.description = queryResponse['item']['description']
            self.image_id = queryResponse['item']['image_id']
            self.tags = queryResponse['item']['tags']
            self.exists = true
        else:
            self.name = ''
            self.description = ''
            self.image_id = ''
            self.tags = []
            self.exists = false

    def __str__(self):
        return json.dumps({
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'image_id': self.image_id,
            'tags': self.tags
        })

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
        self.exists = false


class RecipeCollection:
    def __new__(self, tags=[]):
        table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])
        condition = None
        queryResult = None
        if tags and len(self.tags) > 0:
            self.tags = tags
            for tag in tags:
                if condition is None:
                    condition = Attr('tags').contains(tag)
                else:
                    condition = Or(condition, Attr('tags').contains(tag))
            queryResult = self.table.scan(FilterExpression=condition)
        else:
            queryResult = self.table.scan()
        self.recipes = [Recipe(item) for item in queryResult['Items']]
        if not self.tags:
            self.tags = set()
            for recipe in self.recipes:
                for tag in recipe.tags:
                    self.tags.add(tag)

    def __str__(self):
        return json.dumps({
            'recipes': self.recipes,
            'tags': self.tags
        })
