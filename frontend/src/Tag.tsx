import { Dispatch, SetStateAction } from "react";
import { ThemeType } from "./ThemeType";
import "./Tag.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { APIRecipePrevew } from "./APIModel";

function Tag({
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
        <div className={"Tag Tag-" + themeType}>
            #{tag}
            <FontAwesomeIcon id={tag} icon={faX} onClick={removeTag(tag)} />
        </div>
    );
}

export default Tag;