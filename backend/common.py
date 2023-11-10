def build_response_body(code, text, headers={}):
    return {
            statusCode: code,
            body: text,
            headers: headers
    }
