interface InternalRecipe {
    title: string,
    imageId: string | null,
    description: string,
    tags?: string[],
}

export type { InternalRecipe }