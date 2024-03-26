import { GroupBase } from "react-select";
import { Dispatch } from "react";
import "./Header.css";
import "./InputLabel.css";
import "./ThemeSelector.css";
import { ThemeType } from "./ThemeType";
import Select from "react-select";

function Header({
  themeType,
  setThemeType,
}: {
  themeType: ThemeType;
  setThemeType: Dispatch<ThemeType>;
}) {
  const options: GroupBase<string>[] = [];
  Object.values(ThemeType).forEach((tt) => {
    options.push({
      options: [tt],
      label: tt,
    });
  });

  return (
    <div className={"Header Header-" + themeType}>
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
  );
}

export default Header;
