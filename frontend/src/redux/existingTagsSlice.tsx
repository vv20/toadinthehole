import { createSlice } from "@reduxjs/toolkit";

interface ExistingTagsState {
    existingTags: string[]
}

const initialState: ExistingTagsState = {
    existingTags: []
}

export const existingTagsSlice = createSlice({
    name: 'existingTags',
    initialState: initialState,
    reducers: {
        addExistingTag: (state, action) => {
            state.existingTags.push(action.payload.tag);
        },
        setExistingTags: (state, action) => {
            state.existingTags = action.payload.tags
        },
    }
})

export const { addExistingTag, setExistingTags } = existingTagsSlice.actions

export default existingTagsSlice.reducer