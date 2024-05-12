from __future__ import annotations

import pytest

from pzsm.db import sync, update_enabled
from SteamAPI import Mod
from SteamAPI.model import PublishedFileDetails


@pytest.mark.unit
def test_sync(fixture_db):
    input_mod_json, con = fixture_db
    mod = Mod(PublishedFileDetails(**input_mod_json))

    sync([mod])

    cursor = con.cursor().execute("SELECT * FROM mods")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][0] == mod.workshop_id

    cursor.execute("SELECT * FROM mod_ids")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][2] == 1

    update_enabled(mod.workshop_id, mod.mod_ids[0].id, False)

    cursor.execute("SELECT * FROM mod_ids")
    result = cursor.fetchall()
    assert result[0][2] == 0


@pytest.mark.unit
def test_update_enabled():
    pass
