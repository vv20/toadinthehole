import { ChangeEvent, Dispatch, ReactNode, useState } from "react";
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
import { APIMethod, callAPI } from "./APIService";
import ClearActiveRecipeButton from "./ClearActiveRecipeButton";

function RecipeEditor({
  themeType,
  recipe,
  existingTags,
  setActiveRecipe
}: {
  themeType: ThemeType;
  recipe: APIRecipePrevew;
  existingTags: string[];
  setActiveRecipe: Dispatch<ReactNode>;
}) {
  const [formData, setFormData] = useState<APIRecipePrevew>(recipe);

  function handleChange(
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
  }

  function submitRecipe() {
    callAPI({
      path: '/recipe',
      apiMethod: APIMethod.POST,
      requestBody: formData,
      parseResponseJson: false
    })
  }

  return (
    <div className={"RecipeEditor RecipeEditor-" + themeType}>
      <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
        <input
          name="name"
          type="text"
          placeholder={formData.name}
          className={
            "InputField InputField-" +
            themeType +
            " RecipeTitle RecipeTitle-" +
            themeType
          }
          onChange={handleChange}
        />
        <ClearActiveRecipeButton themeType={themeType} setActiveRecipe={setActiveRecipe} />
      </div>
      <div style={{display: 'flex'}}>
        <div className={"RecipeEditorLeft RecipeEditorLeft-" + themeType}>
          <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
            <ImageUpload themeType={themeType} imageId={formData.imageId} setFormData={setFormData}/>
          </div>
          <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
            <textarea
              name="description"
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
            <TagEditor
              themeType={themeType}
              tags={formData.tags}
              existingTags={existingTags}
              setFormData={setFormData} />
          </div>
          <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
            <button className={"Button Button-" + themeType} onClick={submitRecipe}>Submit</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RecipeEditor;
