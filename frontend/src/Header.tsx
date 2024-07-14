import { Dispatch, ReactNode } from "react";
import Select, { GroupBase } from "react-select";
import "./Header.css";
import "./InputLabel.css";
import "./HeaderLeft.css";
import "./HeaderRight.css";
import NewRecipeButton from "./NewRecipeButton";
import "./ThemeSelector.css";
import { ThemeType } from "./ThemeType";

function Header({
  themeType,
  isLoggedIn,
  existingTags,
  setThemeType,
  setActiveRecipe,
}: {
  themeType: ThemeType;
  isLoggedIn: boolean;
  existingTags: string[];
  setThemeType: Dispatch<ThemeType>;
  setActiveRecipe: Dispatch<ReactNode>;
}) {
  const options: GroupBase<string>[] = [];
  Object.values(ThemeType).forEach((tt) => {
    options.push({
      options: [tt],
      label: tt,
    });
  });

  const leftChildren: ReactNode[] = [];
  if (isLoggedIn) {
    leftChildren.push(
      <NewRecipeButton
        themeType={themeType}
        existingTags={existingTags}
        setActiveRecipe={setActiveRecipe}
      />
    );
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
            setThemeType(ThemeType[newValue as keyof typeof ThemeType])
          }
        />
      </div>
    </div>
  );
}

export default Header;
