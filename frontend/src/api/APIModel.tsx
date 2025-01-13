type DocumentType = null | boolean | number | string | DocumentType[] | {
    [prop: string]: DocumentType;
};

type APIRecipePreview = {
    slug?: string;
    name?: string;
    image_id?: string;
    description?: string;
    tags?: string[];
}

type APINewImageInfo = {
    imageId?: string;
    presignedUrl?: string;
}

export type { APINewImageInfo, APIRecipePreview, DocumentType };