import { get, post } from "aws-amplify/api";
import { fetchAuthSession } from "aws-amplify/auth";
import { DocumentType } from "./APIModel";

enum APIMethod {
    GET,
    POST,
}

type APICallArguments = {
    path: string;
    apiMethod: APIMethod;
    requestBody?: DocumentType | FormData;
    parseResponseJson: boolean;
}

async function callAPI({
    path,
    apiMethod,
    requestBody,
    parseResponseJson
}: APICallArguments): Promise<DocumentType> {
    const { idToken } = (await fetchAuthSession()).tokens ?? {};
    const options = {
        headers: {
            Authorization: `${idToken?.toString()}`,
        },
        body: requestBody,
    };
    var methodFn;
    switch (apiMethod) {
        case APIMethod.GET: {
            methodFn = get;
            break;
        }
        case APIMethod.POST: {
            methodFn = post;
            break;
        }
    }
    const restOperation = methodFn({
        apiName: "ToadInTheHoleAPI",
        path: path,
        options: options,
    });
    const { body } = await restOperation.response;
    if (parseResponseJson) {
        return body.json();
    }
    else {
        return body.text();
    }
}

export { callAPI, APIMethod }