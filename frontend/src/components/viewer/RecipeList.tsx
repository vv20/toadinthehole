import { Dispatch, ReactNode, useEffect, useState } from "react";

import RecipePreview from "./RecipePreview";
import { APIRecipePrevew, DocumentType } from "../../api/APIModel";
import { APIMethod, callAPI, APICallResponse } from "../../api/APIService";
import { ThemeType } from "../../util/ThemeType";

import "../../styles/viewer/RecipeList.css";

function RecipeList({
    themeType,
    activeRecipe,
    existingTags,
    setActiveRecipe,
    setExistingTags,
}: {
    themeType: ThemeType;
    activeRecipe: ReactNode;
    existingTags: string[];
    setActiveRecipe: Dispatch<ReactNode>;
    setExistingTags: Dispatch<string[]>;
}) {
    const [recipes, setRecipes] = useState<Array<ReactNode>>([]);
    
    useEffect(() => {
        const fetchRecipes = async () => {
            try {
                const recipeResponse: APICallResponse = await callAPI({
                    'path': '/collection',
                    'apiMethod': APIMethod.GET,
                    parseResponseJson: true,
                });
                if (!recipeResponse.success) {
                    // TODO: alert the user
                    return;
                }
                const recipeJson = recipeResponse.payload as {[key: string]: DocumentType};
                const recipePreviews: APIRecipePrevew[] = recipeJson.recipes as APIRecipePrevew[];
                const recipePreviewNodes: ReactNode[] = [];
                
                if (recipePreviews.length === recipes.length) {
                    // recipes already set - avoid infinite loop
                    return;
                }
                
                for (var i = 0; i < recipePreviews.length; i++) {
                    recipePreviewNodes.push(
                        <RecipePreview
                        themeType={themeType}
                        preview={recipePreviews[i]}
                        existingTags={existingTags}
                        setActiveRecipe={setActiveRecipe}/>
                    );
                }
                setRecipes(recipePreviewNodes);
                setExistingTags(recipeJson.tags as string[]);
            } catch (e) {
                console.log("Error while fetching recipes:", e);
            }
        };
        fetchRecipes();
    }, [themeType, existingTags, recipes.length, setActiveRecipe, setExistingTags]);
    
    return (
        <div className={"RecipeList RecipeList-" + themeType}>
        <h1 className={"PageTitle PageTitle-" + themeType}>Recipes:</h1>
        {activeRecipe}
        <div style={{display: 'flex', flexWrap: 'wrap'}}>
        {recipes}
        </div>
        </div>
    );
}

export default RecipeList;
