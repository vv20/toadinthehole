import { ChangeEvent, useState } from "react";
import { APIRecipePrevew } from "./APIModel";
import "./InputField.css";
import "./RecipeDescription.css";
import "./RecipeEditor.css";
import "./RecipeFormRow.css";
import "./RecipeTitle.css";
import { ThemeType } from "./ThemeType";

function RecipeEditor({
  themeType,
  recipe,
}: {
  themeType: ThemeType;
  recipe: APIRecipePrevew;
}) {
  const [formData, setFormData] = useState({
    title: recipe.title ? recipe.title : "Recipe Title",
    description: recipe.description ? recipe.description : "",
  });

  function handleChange(
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
  }

  return (
    <div className={"RecipeEditor RecipeEditor-" + themeType}>
      <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <input
          type="text"
          placeholder={formData.title}
          className={
            "InputField InputField-" +
            themeType +
            " RecipeTitle RecipeTitle-" +
            themeType
          }
          onChange={handleChange}
        />
      </div>
      <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <textarea
          placeholder={formData.description}
          className={
            "InputField InputField-" +
            themeType +
            " RecipeDescription RecipeDescription-" +
            themeType
          }
          onChange={handleChange}
        />
      </div>
    </div>
  );
}

export default RecipeEditor;
