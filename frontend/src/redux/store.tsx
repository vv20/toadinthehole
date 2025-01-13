import { configureStore } from "@reduxjs/toolkit";

import activeRecipeReducer from "./activeRecipeSlice";
import existingTagsReducer from "./existingTagsSlice";
import userInfoReducer from "./userInfoSlice";
import recipesReducer from "./recipesSlice";
import themeReducer from './themeSlice';

export const store = configureStore({
    reducer: {
        activeRecipe: activeRecipeReducer,
        existingTags: existingTagsReducer,
        userInfo: userInfoReducer,
        recipes: recipesReducer,
        theme: themeReducer,
    },
})

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch