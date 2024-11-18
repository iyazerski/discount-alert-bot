from pydantic import AnyUrl, BaseModel, field_validator


class AddProductModel(BaseModel):
    product_link: AnyUrl
    discount: float

    @field_validator("discount")
    def discount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Discount must be a positive number.")
        return v


class RemoveProductModel(BaseModel):
    product_link: AnyUrl
