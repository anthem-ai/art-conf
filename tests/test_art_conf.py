import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, call, patch

import pytest
from _pytest.monkeypatch import MonkeyPatch

from art_conf.art_conf import main


@pytest.mark.skip(reason="Currently not writing npmrc or pypirc")
@patch("subprocess.run")
@patch("builtins.input", side_effect=["test.url", "test_user", "test@email.com"])
@patch("getpass.getpass", lambda prompt: "test-pass")
def test_creates_both_rc_files(
    getpass: MagicMock, run: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    with TemporaryDirectory() as dir:

        monkeypatch.setattr(Path, "home", lambda: Path(dir))
        npmrc = Path(dir).joinpath(".npmrc")
        pypirc = Path(dir).joinpath(".pypirc")

        with patch.object(sys, "argv", ["art-conf"]):
            main()

        assert "test.url/npm/npm/" in npmrc.read_text()
        assert "test@email.com" in npmrc.read_text()
        assert "test.url/pypi/pypi" in pypirc.read_text()


@patch("subprocess.run")
@patch("builtins.input", side_effect=["test.url", "test_user", "test@email.com"])
@patch("getpass.getpass", lambda prompt: "test-pass")
def test_runs_pip_config(
    getpass: MagicMock, run: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    with TemporaryDirectory() as dir:

        monkeypatch.setattr(Path, "home", lambda: Path(dir))
        with patch.object(sys, "argv", ["art-conf"]):
            main()

        call1 = call(
            [
                sys.executable,
                "-m",
                "pip",
                "config",
                "set",
                "global.extra-index",
                "https://test_user:test-pass@test.url/pypi/pypi/simple",
            ]
        )

        call2 = call(
            [
                sys.executable,
                "-m",
                "pip",
                "config",
                "set",
                "global.extra-index-url",
                "https://test_user:test-pass@test.url/pypi/pypi/simple",
            ]
        )

        run.assert_has_calls([call1, call2], any_order=True)


@pytest.mark.skip(reason="Currently not writing npmrc or pypirc")
@patch("subprocess.run")
@patch("builtins.input", side_effect=["test.url", "test_user", "test@email.com"])
@patch("getpass.getpass", lambda prompt: "test-pass")
def test_pypirc_exists(
    getpass: MagicMock, run: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    with TemporaryDirectory() as dir:

        monkeypatch.setattr(Path, "home", lambda: Path(dir))
        pypirc = Path(dir).joinpath(".pypirc")
        pypirc.write_text("existing text")

        with patch.object(sys, "argv", ["art-conf"]):
            main()

        assert "existing text" == pypirc.read_text()


@pytest.mark.skip(reason="Currently not writing npmrc or pypirc")
@patch("subprocess.run")
@patch("builtins.input", side_effect=["test.url", "test_user", "test@email.com"])
@patch("getpass.getpass", lambda prompt: "test-pass")
def test_npmrc_exists(
    getpass: MagicMock, run: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    with TemporaryDirectory() as dir:

        monkeypatch.setattr(Path, "home", lambda: Path(dir))
        npmrc = Path(dir).joinpath(".npmrc")
        npmrc.write_text("existing text")

        with patch.object(sys, "argv", ["art-conf"]):
            main()

        assert "existing text" == npmrc.read_text()


@pytest.mark.skip(reason="Currently not writing npmrc or pypirc")
@patch("subprocess.run")
@patch("builtins.input", side_effect=["test.url", "test_user", "test@email.com"])
@patch("getpass.getpass", lambda prompt: "test-pass")
def test_missing_directory(
    getpass: MagicMock, run: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    with TemporaryDirectory() as dir:

        path = Path(dir).joinpath("missing").joinpath("directory")
        monkeypatch.setattr(Path, "home", lambda: path)
        assert not path.is_dir()

        with patch.object(sys, "argv", ["art-conf"]):
            main()

        assert path.is_dir()


@pytest.mark.skip(reason="Currently not writing npmrc or pypirc")
@patch("subprocess.run")
@patch("builtins.input", side_effect=["test_user", "test@email.com"])
@patch("getpass.getpass", lambda prompt: "test-pass")
def test_url_from_argv(
    getpass: MagicMock, run: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    with TemporaryDirectory() as dir:

        monkeypatch.setattr(Path, "home", lambda: Path(dir))
        pypirc = Path(dir).joinpath(".pypirc")

        with patch.object(sys, "argv", ["art-conf", "test.url"]):
            main()

        assert "test.url/pypi/pypi" in pypirc.read_text()
