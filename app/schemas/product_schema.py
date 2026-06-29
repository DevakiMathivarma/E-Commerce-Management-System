from pydantic import BaseModel,Field,ConfigDict,field_validator


# product base schema

class ProductBase(BaseModel):
    name:str=Field(...,min_length=2,max_length=150)
    description:str=Field(...,min_length=5,max_length=500)
    price:float=Field(...,gt=0)
    stock:int=Field(...,ge=0)
    category:str=Field(...,min_length=2,max_length=100)

    @field_validator("name","category")
    @classmethod
    def validate_text(cls,value):
        if not value.strip():
            raise ValueError("field cannot be empty")
        return value.title()


# create product schema

class ProductCreate(ProductBase):
    pass


# update product schema

class ProductUpdate(ProductBase):
    is_active:bool


# product response schema

class ProductResponse(ProductBase):
    id:int
    is_active:bool

    model_config=ConfigDict(from_attributes=True)


# product list schema

class ProductList(BaseModel):
    total_records:int
    current_page:int
    limit:int
    data:list[ProductResponse]