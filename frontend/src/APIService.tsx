import { get, post } from "aws-amplify/api";
import { fetchAuthSession } from "aws-amplify/auth";
import { DocumentType } from "./APIModel";

enum APIMethod {
    GET,
    POST,
}

async function callAPI({ path, apiMethod }: { path: string, apiMethod: APIMethod }): Promise<DocumentType> {
    const { idToken } = (await fetchAuthSession()).tokens ?? {};
    const options = {
        headers: {
            Authorization: `${idToken?.toString()}`,
        },
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
    return body.json();
}

export { callAPI, APIMethod }