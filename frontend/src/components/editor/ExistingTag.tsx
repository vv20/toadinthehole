import { Dispatch } from "react";

import { ThemeType } from "../../util/ThemeType";

import "../../styles/editor/ExistingTag.css";

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