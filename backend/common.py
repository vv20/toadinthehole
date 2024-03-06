import traceback


def build_response_body(code, text, headers={}):
    return {
            'statusCode': code,
            'body': text,
            'headers': headers
    }

def create_handler(method_dict):
    def handler(event, context):
        if event['httpMethod'] not in method_dict:
            return build_response_body(400, 'HTTP method not supported')
        try:
            return method_dict[event['httpMethod']](event)
        except:
            print(traceback.format_exc())
            return build_response_body(500, 'Internal server error')
        
    return handler
