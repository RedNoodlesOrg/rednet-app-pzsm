# Copyright (C) 2013 Peter Rowlands
# Edited by Fakeapate
"""Source server RCON communications module."""

from __future__ import annotations

import itertools
import socket
import struct
import time

# Packet types
SERVERDATA_AUTH = 3
SERVERDATA_AUTH_RESPONSE = 2
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_RESPONSE_VALUE = 0


class RconPacket:
    """RCON packet."""

    def __init__(self, pkt_id=0, pkt_type=-1, body: str | bytes = ""):
        """Init of RconPacket.

        Args:
            pkt_id (int, optional): Id of packet. Defaults to 0.
            pkt_type (int, optional): Type of packet. Defaults to -1.
            body (str | bytes, optional): body content of packet. Defaults to "".
        """
        self.pkt_id = pkt_id
        self.pkt_type = pkt_type
        self.body = body

    def __str__(self):
        """Return the body string."""
        return self.body

    def size(self):
        """Return the pkt_size field for this packet."""
        return len(self.body) + 10

    def pack(self):
        """Return the packed version of the packet."""
        return struct.pack(
            f"<3i{len(self.body) + 2}s",
            self.size(),
            self.pkt_id,
            self.pkt_type,
            bytearray(self.body, "utf-8") if isinstance(self.body, str) else self.body,
        )


class RconConnection:
    """RCON client to server connection."""

    def __init__(self, server, port=27015, password="", single_packet_mode=False):
        """Construct an RconConnection.

        Parameters:
            server (str) server hostname or IP address
            port (int) server port number
            password (str) server RCON password
            single_packet_mode (bool) set to True for servers which do not hand 0-length
                SERVERDATA_RESPONSE_VALUE requests (i.e. Factorio).

        """
        self.server = server
        self.port = port
        self.single_packet_mode = single_packet_mode
        self._sock = socket.create_connection((server, port))
        self.pkt_id = itertools.count(1)
        self._authenticate(password)

    def _authenticate(self, password):
        """Authenticate with the server using the given password."""
        auth_pkt = RconPacket(next(self.pkt_id), SERVERDATA_AUTH, password)
        self._send_pkt(auth_pkt)
        auth_resp = self.read_response(auth_pkt)
        if auth_resp.pkt_type == SERVERDATA_RESPONSE_VALUE:
            auth_resp = self.read_response()
        if auth_resp.pkt_type != SERVERDATA_AUTH_RESPONSE:
            raise RconError("Received invalid auth response packet")
        if auth_resp.pkt_id == -1:
            raise RconAuthError("Bad password")

    def exec_command(self, command):
        """Execute the given RCON command.

        Parameters:
            command (str) the RCON command string (ex. "status")

        Returns the response body
        """
        cmd_pkt = RconPacket(next(self.pkt_id), SERVERDATA_EXECCOMMAND, command)
        self._send_pkt(cmd_pkt)
        resp = self.read_response(cmd_pkt, True)
        return resp.body

    def _send_pkt(self, pkt):
        """Send one RCON packet over the connection.

        Raises:
            RconSizeError if the size of the specified packet is > 4096 bytes
        """
        if pkt.size() > 4096:
            raise RconSizeError("pkt_size > 4096 bytes")
        data = pkt.pack()
        self._sock.sendall(data)

    def _recv_pkt(self):
        """Read one RCON packet."""
        while True:
            header = self._sock.recv(struct.calcsize("<3i"))
            time.sleep(0.01)
            if len(header) != 0:
                break

        (pkt_size, pkt_id, pkt_type) = struct.unpack("<3i", header)
        body = self._sock.recv(pkt_size - 8)
        return RconPacket(pkt_id, pkt_type, body)

    def read_response(self, request=None, multi=False):
        """Return the next response packet.

        Parameters:
            request (RconPacket) if request is provided,
            read_response() will check that the response ID matches the specified request ID,
            multi (bool) set to True if read_response() should check for a multi packet response.
                If the current RconConnection has single_packet_mode enabled,
                this parameter is ignored.

        Raises:
            RconError if an error occurred while receiving the server response
        """
        if request and not isinstance(request, RconPacket):
            raise TypeError("Expected RconPacket type for request")
        if not self.single_packet_mode and multi:
            if not request:
                raise ValueError("Must specify a request packet in order to read a multi-packet response")
            response = self._read_multi_response(request)
        else:
            response = self._recv_pkt()
        if not self.single_packet_mode and response.pkt_type not in (
            SERVERDATA_RESPONSE_VALUE,
            SERVERDATA_AUTH_RESPONSE,
        ):
            raise RconError("Received unexpected RCON packet type")
        if request and response.pkt_id != request.pkt_id:
            raise RconError("Response ID does not match request ID")
        return response

    def _read_multi_response(self, req_pkt: RconPacket):
        """Return concatenated multi-packet response."""
        chk_pkt = RconPacket(next(self.pkt_id), SERVERDATA_RESPONSE_VALUE)
        self._send_pkt(chk_pkt)
        # According to the Valve wiki, a server will mirror a
        # SERVERDATA_RESPONSE_VALUE packet and then send an additional response
        # packet with an empty body. So we should concatenate any packets until
        # we receive a response that matches the ID in chk_pkt
        body_parts: list[bytes | str] = []
        while True:
            response = self._recv_pkt()
            if response.pkt_type != SERVERDATA_RESPONSE_VALUE:
                raise RconError("Received unexpected RCON packet type")
            if response.pkt_id == chk_pkt.pkt_id:
                break
            elif response.pkt_id != req_pkt.pkt_id:
                raise RconError("Response ID does not match request ID")
            body_parts.append(response.body)
        # Read and ignore the extra empty body response
        self._recv_pkt()
        body_parts_strings = []
        for part in body_parts:
            body_parts_strings.append(part.decode() if isinstance(part, bytes) else part)
        return RconPacket(
            req_pkt.pkt_id,
            SERVERDATA_RESPONSE_VALUE,
            "".join(body_parts_strings),
        )


class RconError(Exception):
    """Generic RCON error."""


class RconAuthError(RconError):
    """Raised if an RCON Authentication error occurs."""


class RconSizeError(RconError):
    """Raised when an RCON packet is an illegal size."""
