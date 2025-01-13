import { ChangeEvent, useState } from "react";

import ImageUpload from "./ImageUpload";
import TagEditor from "./TagEditor";
import ClearActiveRecipeButton from "../viewer/ClearActiveRecipeButton";
import { APIRecipePreview } from "../../api/APIModel";
import { APICallResponse, APIMethod, callAPI } from "../../api/APIService";
import { clearActiveRecipe } from "../../redux/activeRecipeSlice";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/container/RecipeEditorLeft.css";
import "../../styles/container/RecipeEditorRight.css";
import "../../styles/container/RecipeFormRow.css";
import "../../styles/editor/RecipeEditor.css";
import "../../styles/general/InputField.css";
import "../../styles/viewer/RecipeDescription.css";
import "../../styles/viewer/RecipeTitle.css";

function RecipeEditor({ recipe }: { recipe?: APIRecipePreview }) {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    const [formData, setFormData] = useState<APIRecipePreview>(recipe ? recipe : {});
    
    function handleChange(
        event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
    }
    
    async function submitRecipe() {
        const path = recipe ? recipe.slug ? '/recipe?recipeID=' + recipe.slug : '/recipe' : '/recipe';
        const response: APICallResponse = await callAPI({
            path: path,
            apiMethod: APIMethod.POST,
            requestBody: formData,
            parseResponseJson: false
        });
        if (!response.success) {
            // TODO: alert the user
            return;
        }
        dispatch(clearActiveRecipe());
    }
    
    async function deleteRecipe() {
        const path = recipe ? recipe.slug ? '/recipe?recipeID=' + recipe.slug : '/recipe' : '/recipe';
        const response: APICallResponse = await callAPI({
            path: '/recipe?recipeID=' + path,
            apiMethod: APIMethod.DELETE,
            requestBody: {},
            parseResponseJson: false
        });
        if (!response.success) {
            // TODO: alert the user
            return;
        }
        dispatch(clearActiveRecipe());
    }
    
    return (
        <div className={"RecipeEditor RecipeEditor-" + themeType}>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <input
        name="name"
        type="text"
        placeholder={formData.name}
        className={
            "InputField InputField-" +
            themeType +
            " RecipeTitle RecipeTitle-" +
            themeType
        }
        onChange={handleChange}
        />
        <ClearActiveRecipeButton/>
        </div>
        <div style={{display: 'flex'}}>
        <div className={"RecipeEditorLeft RecipeEditorLeft-" + themeType}>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <ImageUpload imageId={formData.image_id} setFormData={setFormData}/>
        </div>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <textarea
        name="description"
        placeholder={formData.description}
        className={
            "InputField InputField-" +
            themeType +
            " RecipeDescription RecipeDescription-" +
            themeType
        }
        onChange={handleChange}
        />
        </div>
        </div>
        <div className={"RecipeEditorRight RecipeEditorRight-" + themeType}>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <TagEditor tags={formData.tags} setFormData={setFormData}/>
        </div>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <button className={"Button Button-" + themeType} onClick={deleteRecipe}>Delete</button>
        <button className={"Button Button-" + themeType} onClick={submitRecipe}>Submit</button>
        </div>
        </div>
        </div>
        </div>
    );
}

export default RecipeEditor;
