import traceback


def build_response_body(code, text, event, headers={}):
    headers['Access-Control-Allow-Origin'] = '*'
    return {
            'statusCode': code,
            'body': text,
            'headers': headers
    }

def create_handler(method_dict):
    def handler(event, context):
        if event['httpMethod'] not in method_dict:
            return build_response_body(400, 'HTTP method not supported', event)
        try:
            return method_dict[event['httpMethod']](event)
        except:
            print(traceback.format_exc())
            return build_response_body(500, 'Internal server error', event)
        
    return handler
