import { ChangeEvent, Dispatch, KeyboardEvent, ReactNode, SetStateAction } from "react";

import ActiveTag from "./ActiveTag";
import ExistingTag from "./ExistingTag";
import { APIRecipePreview } from "../../api/APIModel";
import { useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/editor/NewTag.css";
import "../../styles/editor/TagEditor.css";

function TagEditor({
    tags,
    setFormData,
}: {
    tags?: string[],
    setFormData: Dispatch<SetStateAction<APIRecipePreview>>,
}) {
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;
    const existingTags: string[] = useAppSelector((state) => state.existingTags).existingTags;

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
                tag={tags[i]}
                setFormData={setFormData} 
                />
            );
        }
    }
    
    const existingTagElements: Array<ReactNode> = [];
    for (i = 0; i < existingTags.length; i++) {
        existingTagElements.push(
            <ExistingTag tag={existingTags[i]} createNewTag={createNewTag}/>
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