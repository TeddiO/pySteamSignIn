import unittest
import sys
import os
import logging
from unittest.mock import patch
import urllib.error
import socket

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
from pysteamsignin.steamsignin import SteamSignIn


def valid_results():
    steam_id = "12345678901234567"
    claimed = f"https://steamcommunity.com/openid/id/{steam_id}"

    return {
        "openid.assoc_handle": "assoc",
        "openid.signed": "claimed_id,identity",
        "openid.sig": "sig",
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.claimed_id": claimed,
        "openid.identity": claimed,
    }


class FakeSteamResponse:
    def __init__(self, body):
        self._body = body.encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class TestSteamSignIn(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_valid_openid_response_returns_steamid_string(self, mock_urlopen):
        mock_urlopen.return_value = FakeSteamResponse("is_valid:true\n")

        signin = SteamSignIn()
        result = signin.ValidateResults(valid_results())

        self.assertEqual(result, "12345678901234567")

    @patch("urllib.request.urlopen")
    def test_steam_is_valid_false_denies_login(self, mock_urlopen):
        mock_urlopen.return_value = FakeSteamResponse("is_valid:false\n")

        signin = SteamSignIn()
        result = signin.ValidateResults(valid_results())

        self.assertFalse(result)

    @patch("urllib.request.urlopen", side_effect = socket.timeout("timed out"))
    def test_openid_timeout_fails_closed_and_logs_warning(self, mock_urlopen):
        with self.assertLogs("pysteamsignin.steamsignin", level = logging.WARNING) as logs:
            signin = SteamSignIn()
            result = signin.ValidateResults(valid_results())

        self.assertFalse(result)
        self.assertIn("Steam OpenID verification failed", logs.output[0])

    @patch("urllib.request.urlopen", side_effect = urllib.error.URLError("connection failed"))
    def test_network_error_fails_closed_and_logs_warning(self, mock_urlopen):
        with self.assertLogs("pysteamsignin.steamsignin", level = logging.WARNING) as logs:
            signin = SteamSignIn()
            result = signin.ValidateResults(valid_results())

        self.assertFalse(result)
        self.assertIn("Steam OpenID verification failed", logs.output[0])

    @patch("urllib.request.urlopen")
    def test_claimed_id_identity_mismatch_fails_validation(self, mock_urlopen):
        mock_urlopen.return_value = FakeSteamResponse("is_valid:true\n")

        results = valid_results()
        results["openid.identity"] = "https://steamcommunity.com/openid/id/DIFFERENT"

        signin = SteamSignIn()
        result = signin.ValidateResults(results)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
