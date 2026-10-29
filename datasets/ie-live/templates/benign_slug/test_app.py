from app import slugify


def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("Ada Lovelace!") == "ada-lovelace"
    assert slugify("already-ok") == "already-ok"
