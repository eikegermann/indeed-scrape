from typer.testing import CliRunner

from scrape import app

runner = CliRunner()

def test_app():
    result = runner.invoke(app, ["scrape", "--job", "data scientist"])
    assert result.exit_code == 0