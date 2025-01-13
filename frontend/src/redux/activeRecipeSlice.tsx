import { createSlice } from "@reduxjs/toolkit";

import ActiveRecipeType from "../util/ActiveRecipeType";

interface ActiveRecipeState {
    activeRecipeType: ActiveRecipeType,
    activeRecipeSlug?: string
}

const initialState: ActiveRecipeState = {
    activeRecipeType: ActiveRecipeType.None
}

export const activeRecipeSlice = createSlice({
    name: 'activeRecipe',
    initialState: initialState,
    reducers: {
        viewRecipe: (state, action) => {
            state.activeRecipeType = ActiveRecipeType.View;
            state.activeRecipeSlug = action.payload.recipeSlug;
        },
        editRecipe: (state, action) => {
            state.activeRecipeType = ActiveRecipeType.Edit;
            state.activeRecipeSlug = action.payload.recipeSlug;
        },
        clearActiveRecipe: (state) => {
            state.activeRecipeType = ActiveRecipeType.None;
            state.activeRecipeSlug = undefined;
        }
    }
})

export const { viewRecipe, editRecipe, clearActiveRecipe } = activeRecipeSlice.actions

export default activeRecipeSlice.reducer