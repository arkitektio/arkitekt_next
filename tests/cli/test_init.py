import os
import pytest
from arkitekt_next.cli.io import load_manifest_yaml
from arkitekt_next.cli.main import cli
from click.testing import CliRunner

@pytest.fixture
def initialized_app_cli_runner():


    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "init",
                "--identifier",
                "arkitekt-next",
                "--version",
                "0.0.1",
                "--author",
                "arkitek",
                "--template",
                "simple",
                "--scopes",
                "read",
                "--scopes",
                "write",
            ],
        )
        assert result.exit_code == 0, result.output
        yield runner


@pytest.mark.cli
def test_init():
    runner = CliRunner()
    with runner.isolated_filesystem() as td:
        result = runner.invoke(
            cli,
            [
                "init",
                "--identifier",
                "arkitekt_next",
                "--version",
                "0.0.1",
                "--author",
                "arkitek",
                "--template",
                "simple",
                "--scopes",
                "read",
                "--scopes",
                "write",
            ],
        )

        arkitekt_next_folder = os.path.join(td, ".arkitekt_next")

        assert result.exit_code == 0
        assert os.path.exists(arkitekt_next_folder)
        assert os.path.exists(os.path.join(arkitekt_next_folder, "manifest.yaml"))

        manifest = load_manifest_yaml(
            os.path.join(arkitekt_next_folder, "manifest.yaml")
        )
        assert manifest.identifier == "arkitekt_next"
        assert manifest.version == "0.0.1"
        assert manifest.author == "arkitek"
        assert manifest.scopes == ["read", "write"]


@pytest.mark.cli
def test_no_init():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "init",
            ],
        )
        # Second time
        result = runner.invoke(
            cli,
            [
                "init",
            ],
        )

        assert result.exit_code == 1
        assert "Do you want to overwrite" in result.output


@pytest.mark.cli
def test_with_overwrite():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "init",
            ],
        )
        # Second time
        result = runner.invoke(
            cli,
            [
                "init",
                "--overwrite-manifest",
            ],
        )

        assert result.exit_code == 0


@pytest.mark.cli
def test_not_yet_initialized():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["manifest", "scopes", "add", "write"],
        )

        assert result.exit_code == 1
        assert "No manifest found" in result.output
