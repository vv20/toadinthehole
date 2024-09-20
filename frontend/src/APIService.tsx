import { get, post, del } from "aws-amplify/api";
import { fetchAuthSession } from "aws-amplify/auth";
import { DocumentType } from "./APIModel";

enum APIMethod {
    GET,
    POST,
    DELETE,
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
    const args = {
        apiName: "ToadInTheHoleAPI",
        path: path,
        options: {
            headers: {
                Authorization: `${idToken?.toString()}`,
            },
            body: requestBody,
        },
    }

    switch (apiMethod) {
        case APIMethod.GET: {
            const { body } = await get(args).response;
            if (parseResponseJson) {
                return body.json();
            }
            else {
                return body.text();
            }
        }
        case APIMethod.POST: {
            const { body } = await post(args).response;
            if (parseResponseJson) {
                return body.json();
            }
            else {
                return body.text();
            }
        }
        case APIMethod.DELETE: {
            await del(args).response;
            return "OK";
        }
    }
}

export { callAPI, APIMethod }