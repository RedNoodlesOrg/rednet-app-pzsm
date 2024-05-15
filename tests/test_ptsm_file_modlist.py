from __future__ import annotations

import pytest

from pzsm.file_parser.modlist import Modlist
from SteamAPI.mod import Mod


@pytest.fixture
def mock_mod(mocker):
    mock_mod = mocker.Mock(spec=Mod)
    mock_mod.mod_ids = [mocker.Mock(enabled=True, id="123")]
    mock_mod.workshop_id = "456"
    return mock_mod


def test_modlist_init_with_mods(mock_mod):
    modlist = Modlist(mods=[mock_mod])
    assert modlist.mods == [mock_mod]
    assert modlist.modids is None
    assert modlist.workshopids is None


def test_modlist_init_with_ids():
    modlist = Modlist(modids="123", workshopids="456")
    assert modlist.mods is None
    assert modlist.modids == "123"
    assert modlist.workshopids == "456"


def test_modlist_init_with_nothing():
    with pytest.raises(ValueError):
        Modlist()


def test_modlist_init_with_both(mock_mod):
    with pytest.raises(ValueError):
        Modlist(mods=[mock_mod], modids="123", workshopids="456")


def test_get_ids_with_mods(mock_mod):
    modlist = Modlist(mods=[mock_mod])
    modids, workshopids = modlist.get_ids()
    assert modids == "123"
    assert workshopids == "456"


def test_get_ids_with_ids():
    modlist = Modlist(modids="123", workshopids="456")
    modids, workshopids = modlist.get_ids()
    assert modids == "123"
    assert workshopids == "456"


def test_get_ids_with_nothing():
    with pytest.raises(ValueError):
        Modlist()
