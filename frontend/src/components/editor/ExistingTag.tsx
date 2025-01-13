import { Dispatch } from "react";

import { useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/editor/ExistingTag.css";

function ExistingTag({
    tag,
    createNewTag,
}: {
    tag: string,
    createNewTag: Dispatch<string>,
}) {
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

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