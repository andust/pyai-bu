from app.helpers.document.main import format_docs

def test_format_docs(docs):
    formatted = format_docs(docs)
    assert isinstance(formatted, str)
    assert "This is the first document." in formatted
    assert "This is the second document with more content." in formatted
