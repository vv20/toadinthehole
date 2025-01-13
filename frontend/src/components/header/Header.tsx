import { ReactNode } from "react";
import Select, { GroupBase } from "react-select";

import NewRecipeButton from "./NewRecipeButton";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { setTheme } from "../../redux/themeSlice";
import ThemeType from "../../util/ThemeType";

import "../../styles/general/InputLabel.css";
import "../../styles/header/Header.css";
import "../../styles/header/ThemeSelector.css";
import "../../styles/container/HeaderLeft.css";
import "../../styles/container/HeaderRight.css";

function Header() {
    const dispatch = useAppDispatch();
    const isLoggedIn: boolean = useAppSelector(state => state.userInfo).isLoggedIn;
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    const options: GroupBase<string>[] = [];
    Object.values(ThemeType).forEach((tt) => {
        options.push({
            options: [tt],
            label: tt,
        });
    });
    
    const leftChildren: ReactNode[] = [];
    if (isLoggedIn) {
        leftChildren.push(<NewRecipeButton key="newRecipeButton"/>);
    }
    
    return (
        <div className={"Header Header-" + themeType}>
        <div className={"HeaderLeft HeaderLeft-" + themeType}>{leftChildren}</div>
        <div className={"HeaderRight HeaderRight-" + themeType}>
        <label className={"InputLabel InputLabel-" + themeType}>Theme:</label>
        <Select
        className={"ThemeSelector ThemeSelector-" + themeType}
        defaultValue="Pastel"
        options={options}
        onChange={(newValue) =>
            dispatch(setTheme({ theme: ThemeType[newValue as keyof typeof ThemeType] }))
        }
        />
        </div>
        </div>
    );
}

export default Header;
