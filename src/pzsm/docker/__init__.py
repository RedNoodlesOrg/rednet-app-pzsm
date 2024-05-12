"""__init__."""

from __future__ import annotations

import docker


def restart(base_url: str, container_name: str):
    """Restart PZ Server."""
    client = docker.DockerClient(base_url=base_url)
    container = client.containers.get(container_name)

    if container is not None:
        container.restart()
    return container is not None
