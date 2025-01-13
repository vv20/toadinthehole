import { createSlice } from "@reduxjs/toolkit";

interface UserInfoState {
    isLoggedIn: boolean,
    requirePasswordChange: boolean,
    loginError: string,
    username: string,
}

const initialState: UserInfoState = {
    isLoggedIn: false,
    requirePasswordChange: false,
    loginError: "",
    username: "",
}

export const userInfoSlice = createSlice({
    name: 'userInfo',
    initialState: initialState,
    reducers: {
        logIn: (state) => {
            state.isLoggedIn = true;
        },
        logOut: (state) => {
            state.isLoggedIn = false;
        },
        setLogInError: (state, action) => {
            state.loginError = action.payload.loginError;
        },
        setRequirePasswordChange: (state, action) => {
            state.requirePasswordChange = action.payload.requirePasswordChange;
        },
        setUsername: (state, action) => {
            state.username = action.payload.username;
        }
    }
})

export const { logIn, logOut, setLogInError, setRequirePasswordChange, setUsername } = userInfoSlice.actions;

export default userInfoSlice.reducer