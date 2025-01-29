from django.db import models



class PrimeryCategory(models.Model):
    image = models.ImageField(
        verbose_name="تصویر", 
        upload_to="categories/", null=True
    )
    
    name = models.CharField(
        max_length=200,
        verbose_name="دسته بندی اصلی", unique=True
    )
    
    slug = models.SlugField(
        max_length=200,
        verbose_name="اسلاگ", unique=True
    )
    
    
    class Meta:
        verbose_name = "دسته بندی اصلی"
        verbose_name_plural = "دسته بندی های اصلی"
    
    def __str__(self):
        return self.name


class Category(models.Model):
    primery_category = models.ForeignKey(
        PrimeryCategory,
        on_delete=models.CASCADE,
        verbose_name="دسته بندی اصلی", related_name="chiled_category"
    )
    
    name = models.CharField(
        max_length=200,
        verbose_name="دسته بندی", unique=True
    )
    
    slug = models.SlugField(
        max_length=200,
        verbose_name="اسلاگ", unique=True
    )
    
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
    
    def __str__(self):
        return self.name


class Color(models.Model):
    color = models.CharField(
        max_length=200,
        verbose_name="رنگ", unique=True
    )
    
    available = models.BooleanField(verbose_name="موجود", default=True)
     
    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ ها"
    
    def __str__(self):
        return self.color


class ProductDescription(models.Model):
    
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان"
    )
    
    image = models.ImageField(
        verbose_name="تصویر",
        upload_to="product/descriptions/image/", blank=True, null=True
    )
    
    description = models.TextField(verbose_name="توضیحات")
    
    class Meta:
        verbose_name = "توضیحات محصول"
        verbose_name_plural = "توضیحات محصولات"
    
        
    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(
        verbose_name="تصویر",
        upload_to="products/image/"
    )
    
    class Meta:
        verbose_name = "تصاویر محصول"
        verbose_name_plural = "تصاویر محصولات"


class Product(models.Model):
    
    primery_category = models.ForeignKey(
        PrimeryCategory,
        on_delete=models.CASCADE,
        verbose_name="دسته بندی اصلی محصول"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="دسته بندی محصول"
    )
    
    name = models.CharField(
        max_length=200,
        verbose_name="نام محصول", unique=True
    )
    
    slug = models.SlugField(
        max_length=200,
        verbose_name="اسلاگ", unique=True
    )
    
    short_description = models.TextField(
        blank=True, null=True,
        verbose_name="توضیحات مختصر محصول",
        help_text="مقالات، کاربرد محصول و ..."
    )
    
    descriptions = models.ManyToManyField(
        ProductDescription,
        verbose_name="توضیحات محصول", blank=True
    )
    
    image = models.ImageField(
        verbose_name="تصویر اصلی محصول",
        upload_to="products/main/image/"
    )
    
    images = models.ManyToManyField(
        ProductImage,
        related_name='product',
        verbose_name="عکس های محصول", blank=True
    )
    
    colors = models.ManyToManyField(
        Color,
        verbose_name="رنگ های محصول", blank=True
    )
    
    sales = models.IntegerField(verbose_name="فروش", default=0)
    
    price = models.BigIntegerField(verbose_name="قیمت")
    str_price = models.CharField(
        verbose_name="قیمت",
        max_length=200
    )
    
    quantity =models.PositiveIntegerField(verbose_name="تعداد موجود محصول")
    available = models.BooleanField(verbose_name="موجود", default=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['updated']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'{self.category.name}---{self.name}'