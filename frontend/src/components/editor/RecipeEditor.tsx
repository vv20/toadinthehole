import { ChangeEvent, useState } from "react";

import { remove, uploadData } from 'aws-amplify/storage';

import ImageUpload from "./ImageUpload";
import TagEditor from "./TagEditor";
import ClearActiveRecipeButton from "../viewer/ClearActiveRecipeButton";
import { APIRecipePreview } from "../../api/APIModel";
import { APICallResponse, APIMethod, callAPI } from "../../api/APIService";
import { clearActiveRecipe } from "../../redux/activeRecipeSlice";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { addRecipe, removeRecipe } from "../../redux/recipesSlice";
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
    const imageFile: File|undefined = useAppSelector((state) => state.image).imageFile;
    const imageId: string|undefined = useAppSelector((state) => state.image).imageId;

    const [formData, setFormData] = useState<APIRecipePreview>(recipe ? recipe : {});
    
    function handleChange(
        event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) {
        const { name, value } = event.target;
        setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
    }
    
    async function submitRecipe() {
        if (imageId === undefined && formData.image_id !== undefined) {
            // delete the existing image
            await remove({ key: formData.image_id + ".jpg" })
            formData.image_id = undefined
        }

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
        const responseRecipe: string = (typeof response.payload === "string") ? response.payload : JSON.stringify(response.payload);
        dispatch(addRecipe({ recipe: JSON.parse(responseRecipe) }))

        if (imageFile !== undefined && imageId !== undefined) {
            try {
                const result = await uploadData({
                    key: imageId + ".jpg",
                    data: imageFile,
                }).result
                
                // trigger the resizing of the image
                await callAPI({
                    path: "/image/" + imageId,
                    apiMethod: APIMethod.POST,
                    parseResponseJson: false
                });
                
                console.log("Image uploaded: ", result);
                if (setFormData !== undefined) {
                    setFormData((prevFormData) => ({ ...prevFormData, image_id: imageId }));
                }
            }
            catch (error) {
                console.log("Error: ", error);
            }
        }
    }
    
    async function deleteRecipe() {
        const path = recipe ? recipe.slug ? '/recipe?recipeID=' + recipe.slug : '/recipe' : '/recipe';
        const response: APICallResponse = await callAPI({
            path: path,
            apiMethod: APIMethod.DELETE,
            requestBody: {},
            parseResponseJson: false
        });
        if (!response.success) {
            // TODO: alert the user
        }
        dispatch(clearActiveRecipe());
        dispatch(removeRecipe({ recipe: recipe }))
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
        <ImageUpload editable={true}/>
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
