from arkitekt_next.cli.main import cli
import os
from arkitekt_next.cli.io import load_manifest_yaml
import pytest


@pytest.mark.cli
def test_add_scopes(initialized_app_cli_runner):
    result = initialized_app_cli_runner.invoke(
        cli,
        [
            "manifest",
            "scopes",
            "add",
            "write",
        ],
    )

    assert result.exit_code == 0

    manifest = load_manifest_yaml(os.path.join(".arkitekt_next", "manifest.yaml"))
    assert "write" in manifest.scopes


@pytest.mark.cli
def test_list_scopes(initialized_app_cli_runner):
    result = initialized_app_cli_runner.invoke(
        cli,
        [
            "manifest",
            "scopes",
            "list",
        ],
    )

    assert result.exit_code == 0
    assert "read" in result.output


@pytest.mark.cli
def test_advailable_scopes(initialized_app_cli_runner):
    result = initialized_app_cli_runner.invoke(
        cli,
        [
            "manifest",
            "scopes",
            "available",
        ],
    )

    assert result.exit_code == 0
    assert "read" in result.output
    assert "write" in result.output


