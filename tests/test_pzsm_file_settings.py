from __future__ import annotations

from unittest.mock import mock_open, patch

import pytest

from pzsm.file_parser.modlist import Modlist
from pzsm.file_parser.server_settings import ServerSettings


@pytest.fixture
def mock_modlist():
    modlist = Modlist(mods=[])
    modlist.get_ids = lambda: ("mod1;mod2", "workshop1;workshop2")
    return modlist


@pytest.mark.unit
def test_load(fixture_file_parser):
    mock_file_content = fixture_file_parser
    with patch("builtins.open", new_callable=mock_open, read_data="".join(mock_file_content)) as mock_file:
        server_settings = ServerSettings("path/to/file")
        server_settings._load()
        mock_file.assert_called_once_with("path/to/file", encoding="utf-8")
        assert server_settings._file_lines == mock_file_content
        assert server_settings._mods_index == 0
        assert server_settings._workshop_index == 3


@pytest.mark.unit
def test_save(fixture_file_parser):
    mock_file_content = fixture_file_parser
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        server_settings = ServerSettings("path/to/file")
        server_settings._file_lines = mock_file_content
        server_settings._save()
        mock_file.assert_called_once_with("path/to/file", "w", encoding="utf-8")
        mock_file().writelines.assert_called_once_with(mock_file_content)


@pytest.mark.unit
def test_update_mods(mock_modlist, fixture_file_parser):
    mock_file_content = fixture_file_parser
    with patch("builtins.open", new_callable=mock_open, read_data="".join(mock_file_content)) as mock_file:
        server_settings = ServerSettings("path/to/file")
        server_settings.update_mods(mock_modlist)
        mock_file.assert_any_call("path/to/file", encoding="utf-8")
        mock_file.assert_any_call("path/to/file", "w", encoding="utf-8")
        assert server_settings._file_lines[server_settings._mods_index] == "Mods=mod1;mod2\n"
        assert server_settings._file_lines[server_settings._workshop_index] == "WorkshopItems=workshop1;workshop2\n"
