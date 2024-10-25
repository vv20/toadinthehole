import { Dispatch, SetStateAction } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faX } from "@fortawesome/free-solid-svg-icons";

import { APIRecipePrevew } from "../../api/APIModel";
import { ThemeType } from "../../util/ThemeType";

import "../../styles/editor/ActiveTag.css";

function ActiveTag({
    themeType,
    tag,
    setFormData,
}: {
    themeType: ThemeType,
    tag: string,
    setFormData: Dispatch<SetStateAction<APIRecipePrevew>>,
}) {
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
        <div className={"ActiveTag ActiveTag-" + themeType}>
        #{tag}
        <FontAwesomeIcon id={tag} icon={faX} onClick={removeTag(tag)} />
        </div>
    );
}

export default ActiveTag;