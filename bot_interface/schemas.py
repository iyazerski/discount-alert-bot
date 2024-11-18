from pydantic import AnyUrl, BaseModel, field_validator


class AddProductModel(BaseModel):
    url: AnyUrl
    discount: float

    @field_validator("discount")
    def discount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Discount must be a positive number.")
        return v


class RemoveProductModel(BaseModel):
    product_id: int

    @field_validator("product_id")
    def product_id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Product ID must be a positive number.")
        return v


class UpdateProductModel(BaseModel):
    product_id: int
    discount: float

    @field_validator("product_id")
    def product_id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Product ID must be a positive number.")
        return v

    @field_validator("discount")
    def discount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Discount must be a positive number.")
        return v
