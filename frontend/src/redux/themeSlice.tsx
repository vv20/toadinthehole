import { createSlice } from "@reduxjs/toolkit";
import ThemeType from "../util/ThemeType";

interface ThemeState {
    theme: ThemeType
}

const initialState: ThemeState = {
    theme: ThemeType.Pastel
}

export const themeSlice = createSlice({
    name: 'theme',
    initialState: initialState,
    reducers: {
        setTheme: (state, action) => {
            state.theme = action.payload.theme
        }
    }
})

export const { setTheme } = themeSlice.actions

export default themeSlice.reducer