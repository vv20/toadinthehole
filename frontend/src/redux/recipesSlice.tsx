import { createSlice } from "@reduxjs/toolkit";

import { APIRecipePreview } from "../api/APIModel";

interface RecipesState {
    recipes: { [ prop: string ]: APIRecipePreview },
    recipesLoaded: boolean
}

const initialState: RecipesState = {
    recipes: {},
    recipesLoaded: false
}

export const recipesSlice = createSlice({
    name: 'recipes',
    initialState: initialState,
    reducers: {
        addRecipe: (state, action) => {
            state.recipes[action.payload.recipe.slug] = action.payload.recipe;
        },
        removeRecipe: (state, action) => {
            delete state.recipes[action.payload.recipe.slug]
        },
        setRecipes: (state, action) => {
            state.recipes = action.payload.recipes
            state.recipesLoaded = true
        },
    }
})

export const { addRecipe, removeRecipe, setRecipes } = recipesSlice.actions

export default recipesSlice.reducer