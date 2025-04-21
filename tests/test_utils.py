import pytest
from src.utils import Product, Category


def test_product_initialization():
    product = Product("Test Product", "Test Description", 100.0, 10)

    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_initialization():
    product1 = Product("Product 1", "Desc 1", 50.0, 5)
    product2 = Product("Product 2", "Desc 2", 75.0, 3)
    products = [product1, product2]

    category = Category("Test Category", "Test Category Description", products)

    assert category.name == "Test Category"
    assert category.description == "Test Category Description"
    assert category.products == products
    assert len(category.products) == 2


def test_category_count():
    Category.category_count = 0

    product = Product("Product", "Desc", 100.0, 1)
    category1 = Category("Cat1", "Desc1", [product])
    category2 = Category("Cat2", "Desc2", [product])

    assert Category.category_count == 2


def test_product_count():
    product1 = Product("Product 1", "Desc 1", 50.0, 5)
    product2 = Product("Product 2", "Desc 2", 75.0, 3)
    products = [product1, product2]

    category = Category("Test Category", "Test Description", products)

    assert category.product_count == 2
    assert len(category.products) == category.product_count


def test_empty_category():
    category = Category("Empty Category", "No products here", [])

    assert category.name == "Empty Category"
    assert category.description == "No products here"
    assert category.products == []
    assert category.product_count == 0
    assert Category.category_count > 0
