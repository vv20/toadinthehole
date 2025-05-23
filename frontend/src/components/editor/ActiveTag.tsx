import { Dispatch, SetStateAction } from "react";

import { APIRecipePreview } from "../../api/APIModel";
import { useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/editor/ActiveTag.css";

function ActiveTag({
    tag,
    setFormData,
}: {
    tag: string,
    setFormData: Dispatch<SetStateAction<APIRecipePreview>>,
}) {
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    function removeTag(tag: string) {
        return () => {
            setFormData((prevFormData) => {
                const existingTags = prevFormData.tags ? prevFormData.tags : [];
                const indexOfTag = existingTags.indexOf(tag);
                if (indexOfTag < 0) {
                    return prevFormData;
                }
                const newTags = existingTags.slice();
                newTags.splice(indexOfTag, 1);
                return {
                    ...prevFormData,
                    tags: newTags
                };
            });
        };
    }
    
    return (
        <button
        className={"Button Button-" + themeType + " ActiveTag ActiveTag-" + themeType}
        onClick={removeTag(tag)}>
        #{tag}
        </button>
    );
}

export default ActiveTag;