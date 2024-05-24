import { ChangeEvent, Dispatch, KeyboardEvent, ReactNode, SetStateAction } from "react";
import { ThemeType } from "./ThemeType";
import { InternalRecipe } from "./InternalModel";
import Tag from "./Tag";
import "./NewTag.css";
import "./TagEditor.css";

function TagEditor({
  themeType,
  tags,
  setFormData,
}: {
  themeType: ThemeType,
  tags?: string[],
  setFormData: Dispatch<SetStateAction<InternalRecipe>>,
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

  const tagElements: Array<ReactNode> = [];
  if (tags !== undefined) {
    for (var i = 0; i < tags.length; i++) {
      tagElements.push(<Tag themeType={themeType} tag={tags[i]} setFormData={setFormData} />);
    }
  }

  return (
    <div className={"TagEditor TagEditor-" + themeType}>
      <input
        type="text"
        placeholder="#"
        className={"NewTag NewTag-" + themeType}
        onKeyDown={handleEnter}
        onBlur={handleBlur} />
      {tagElements}
    </div>
  );
}

export default TagEditor;