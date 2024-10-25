import { ChangeEvent, Dispatch, KeyboardEvent, ReactNode, SetStateAction } from "react";

import ActiveTag from "./ActiveTag";
import ExistingTag from "./ExistingTag";
import { APIRecipePrevew } from "../../api/APIModel";
import { ThemeType } from "../../util/ThemeType";

import "../../styles/editor/NewTag.css";
import "../../styles/editor/TagEditor.css";

function TagEditor({
    themeType,
    tags,
    existingTags,
    setFormData,
}: {
    themeType: ThemeType,
    tags?: string[],
    existingTags: string[],
    setFormData: Dispatch<SetStateAction<APIRecipePrevew>>,
}) {
    function createNewTag(tag: string) {
        if (tag === "") {
            return;
        }
        setFormData((prevFormData) => {
            const existingTags = prevFormData.tags ? prevFormData.tags : [];
            const tagAlreadyExists = existingTags.indexOf(tag) >= 0;
            if (tagAlreadyExists) {
                return prevFormData;
            }
            return {
                ...prevFormData,
                tags: prevFormData.tags ? prevFormData.tags.concat([tag]) : [tag]
            }
        });
    }
    
    function handleEnter(event: KeyboardEvent<HTMLInputElement>) {
        const { value } = (event.target as EventTarget & HTMLInputElement);
        if (event.key !== "Enter") {
            return;
        }
        (event.target as EventTarget & HTMLInputElement).value = "";
        createNewTag(value);
    }
    
    function handleBlur(event: ChangeEvent<HTMLInputElement>) {
        const { value } = event.target;
        event.target.value = "";
        createNewTag(value);
    }
    
    const activeTagElements: Array<ReactNode> = [];
    if (tags !== undefined) {
        for (var i = 0; i < tags.length; i++) {
            activeTagElements.push(
                <ActiveTag
                themeType={themeType}
                tag={tags[i]}
                setFormData={setFormData} 
                />
            );
        }
    }
    
    const existingTagElements: Array<ReactNode> = [];
    for (i = 0; i < existingTags.length; i++) {
        existingTagElements.push(
            <ExistingTag
            themeType={themeType}
            tag={existingTags[i]}
            createNewTag={createNewTag}
            />
        );
    }
    
    return (
        <div className={"TagEditor TagEditor-" + themeType}>
        <input
        type="text"
        placeholder="#"
        className={"NewTag NewTag-" + themeType}
        onKeyDown={handleEnter}
        onBlur={handleBlur} />
        {activeTagElements}
        {existingTagElements}
        </div>
    );
}

export default TagEditor;