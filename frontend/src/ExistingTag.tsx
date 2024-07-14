import { Dispatch } from "react";
import { ThemeType } from "./ThemeType";
import "./ExistingTag.css";

function ExistingTag({
    themeType,
    tag,
    createNewTag,
}: {
    themeType: ThemeType,
    tag: string,
    createNewTag: Dispatch<string>,
}) {
    function addTagToActive() {
        createNewTag(tag);
    }
    return (
        <button
            className={"ExistingTag ExistingTag-" + themeType}
            onClick={addTagToActive}>
            {tag}
        </button>
    )
}

export default ExistingTag;