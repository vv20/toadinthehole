import { ChangeEvent, useState } from "react";
import { APIRecipePrevew } from "./APIModel";
import "./InputField.css";
import "./RecipeDescription.css";
import "./RecipeEditor.css";
import "./RecipeEditorLeft.css";
import "./RecipeEditorRight.css";
import "./RecipeFormRow.css";
import "./RecipeTitle.css";
import { ThemeType } from "./ThemeType";
import ImageUpload from "./ImageUpload";
import TagEditor from "./TagEditor";
import { InternalRecipe } from "./InternalModel";

function RecipeEditor({
  themeType,
  recipe,
}: {
  themeType: ThemeType;
  recipe: APIRecipePrevew;
}) {
  const [formData, setFormData] = useState<InternalRecipe>({
    title: recipe.title ? recipe.title : "Recipe Title",
    imageId: recipe.imageId ? recipe.imageId : null,
    description: recipe.description ? recipe.description : "",
    tags: recipe.tags,
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
      <div style={{display: 'flex'}}>
        <div className={"RecipeEditorLeft RecipeEditorLeft-" + themeType}>
          <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
            <ImageUpload themeType={themeType} imageId={formData.imageId} setFormData={setFormData}/>
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
        <div className={"RecipeEditorRight RecipeEditorRight-" + themeType}>
          <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
            <TagEditor themeType={themeType} tags={formData.tags} setFormData={setFormData} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default RecipeEditor;
