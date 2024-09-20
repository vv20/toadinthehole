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

type APICallResponse = {
    success: boolean;
    payload: DocumentType;
}

async function callAPI({
    path,
    apiMethod,
    requestBody,
    parseResponseJson
}: APICallArguments): Promise<APICallResponse> {
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
            try {
                const { body, statusCode } = await get(args).response;
                return {
                    success: statusCode >= 200 && statusCode <= 400,
                    payload: parseResponseJson ? await body.json() : await body.text()
                };
            }
            catch (e) {
                console.log(e);
                return {
                    success: false,
                    payload: ""
                }
            }
        }
        case APIMethod.POST: {
            try {
                const { body, statusCode } = await post(args).response;
                return {
                    success: statusCode >= 200 && statusCode <= 400,
                    payload: parseResponseJson ? await body.json() : await body.text()
                };
            }
            catch (e) {
                console.log(e);
                return {
                    success: false,
                    payload: ""
                }
            }
        }
        case APIMethod.DELETE: {
            try {
                const { statusCode } = await del(args).response;
                return {
                    success: statusCode >= 200 && statusCode <= 400,
                    payload: "OK"
                };
            }
            catch (e) {
                console.log(e);
                return {
                    success: false,
                    payload: ""
                }
            }
        }
    }
}

export { callAPI, APIMethod, type APICallResponse }