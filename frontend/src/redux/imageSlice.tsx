import { createSlice } from "@reduxjs/toolkit";
import { v4 as uuidv4 } from 'uuid';

interface ImageState {
    imageFile?: File
    imageId?: string
}

const initialState: ImageState = {
    imageFile: undefined,
    imageId: undefined
}

export const imageSlice = createSlice({
    name: 'image',
    initialState: initialState,
    reducers: {
        clearImage: (state) => {
            state.imageFile = undefined;
            state.imageId = undefined;
        },
        setImage: (state, action) => {
            state.imageFile = undefined;
            state.imageId = action.payload.imageId;
        },
        uploadImage: (state, action) => {
            state.imageFile = action.payload.file;
            state.imageId = uuidv4();
        }
    }
})

export const { clearImage, setImage, uploadImage } = imageSlice.actions

export default imageSlice.reducer