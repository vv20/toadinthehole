import { ReactNode, useEffect } from "react";

import RecipePreview from "./RecipePreview";
import { APIRecipePreview, DocumentType } from "../../api/APIModel";
import { APIMethod, callAPI, APICallResponse } from "../../api/APIService";
import { setExistingTags } from "../../redux/existingTagsSlice";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { setRecipes } from "../../redux/recipesSlice";
import ThemeType from "../../util/ThemeType";

import "../../styles/viewer/RecipeList.css";
import ActiveRecipeContainer from "./ActiveRecipeContainer";

function RecipeList() {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;
    const recipes: { [ prop: string ]: APIRecipePreview } = useAppSelector((state) => state.recipes).recipes;
    const recipesLoaded: boolean = useAppSelector((state) => state.recipes).recipesLoaded;
    
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
                const recipePreviews: APIRecipePreview[] = recipeJson.recipes as APIRecipePreview[];

                const recipePreviewMap: { [ prop: string ]: APIRecipePreview } = {}
                for (let i = 0; i < recipePreviews.length; i++) {
                    const recipePreview: APIRecipePreview = recipePreviews[i];
                    if (recipePreview.slug === undefined) {
                        // TODO: error
                        continue;
                    }
                    recipePreviewMap[recipePreview.slug] = recipePreview
                }
                
                dispatch(setRecipes({ recipes: recipePreviewMap }));
                dispatch(setExistingTags({ tags: recipeJson.tags as string[] }));
            } catch (e) {
                console.log("Error while fetching recipes:", e);
            }
        };
        if (!recipesLoaded) {
            fetchRecipes();
        }
    }, [dispatch, recipesLoaded]);

    const recipePreviewNodes: ReactNode[] = [];
    for (const [, value] of Object.entries(recipes)) {
        recipePreviewNodes.push(<RecipePreview preview={value} />);
    }
    
    return (
        <div className={"RecipeList RecipeList-" + themeType}>
        <h1 className={"PageTitle PageTitle-" + themeType}>Recipes:</h1>
        <ActiveRecipeContainer />
        <div style={{display: 'flex', flexWrap: 'wrap'}}>
        {recipePreviewNodes}
        </div>
        </div>
    );
}

export default RecipeList;
