import { ReactNode } from "react";

import ClearActiveRecipeButton from "./ClearActiveRecipeButton";
import EditButton from "./EditButton";
import { APIRecipePreview } from "../../api/APIModel";
import { useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/container/RecipeFormRow.css";
import "../../styles/editor/ActiveTag.css";
import "../../styles/viewer/Recipe.css";
import "../../styles/viewer/RecipeTitle.css";
import { getImageUrl } from "../../util/UrlUtil";

function Recipe({ preview }: { preview: APIRecipePreview }) {
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    const tagElements: Array<ReactNode> = [];
    if (preview.tags !== undefined) {
        for (var i = 0; i < preview.tags.length; i++) {
            tagElements.push(
                <div className={"ActiveTag ActiveTag-" + themeType}>
                #{preview.tags[i]}
                </div>
            );
        }
    }

    return (
        <div className={"Recipe Recipe-" + themeType}>
        <EditButton preview={preview}/>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <h1 className={"RecipeTitle RecipeTitle-" + themeType}>
        {preview.name}
        </h1>
        <ClearActiveRecipeButton/>
        </div>
        <div style={{display: 'flex'}}>
        <div className={"RecipeEditorLeft RecipeEditorLeft-" + themeType}>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <img
        src={preview.image_id !== undefined ? getImageUrl({ imageId: preview.image_id }) : ""}
        alt="no pic :("
        style={{maxWidth: "100%", height: "auto"}}/>
        </div>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <p>{preview.description}</p>
        </div>
        </div>
        <div className={"RecipeEditorRight RecipeEditorRight-"+ themeType}>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        {tagElements}
        </div>
        </div>
        </div>
        </div>
    );
}

export default Recipe;