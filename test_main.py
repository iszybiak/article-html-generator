import pytest
from main import load_config

def test_load_config_valid_file(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"key": "value"}')

    config = load_config(str(config_file))
    assert config == {"key": "value"}

def test_load_config_missing_file():
    config = load_config("nonexistent.json")
    assert config == {}

def test_load_config_invalid_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text("{invalid json}")

    config = load_config(str(config_file))
    assert config == {}

from main import load_api_key

def test_load_api_key_valid_file(tmp_path):
    api_key_file = tmp_path / "API_KEY"
    api_key_file.write_text("dummy_api_key")

    api_key = load_api_key(str(api_key_file))
    assert api_key == "dummy_api_key"

def test_load_api_key_missing_file():
    api_key = load_api_key("nonexistent_file")
    assert api_key == ""

from main import read_article

def test_read_article_valid_file(tmp_path):
    article_file = tmp_path / "article.txt"
    article_file.write_text("This is a test article.\nNew line.")

    content = read_article(str(article_file))
    assert content == "This is a test article. New line."

def test_read_article_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    content = read_article(str(empty_file))
    assert content is None

def test_read_article_missing_file():
    content = read_article("nonexistent.txt")
    assert content is None

from main import file_cleanup

def test_file_cleanup():
    raw_text = """```html
    <article>Content</article>
    ```"""
    cleaned_text = file_cleanup(raw_text)
    assert cleaned_text == "<article>Content</article>"

from main import save_html_to_file

def test_save_html_to_file(tmp_path):
    output_file = tmp_path / "output.html"
    content = "<html><body>Test</body></html>"

    save_html_to_file(content, str(output_file))
    assert output_file.read_text() == content
