"""Render the HTML preview in headless Chrome and check the viewer comes up.

The page loads CesiumJS and its bundled imagery from cesium.com, so
these tests need a Chrome/Chromium/Edge binary and internet access; they are
skipped otherwise. Set CZML3_BROWSER to the browser executable to choose one.

Pages are served over a local HTTP server, as Jupyter and web servers serve
them. Opened from ``file://``, browsers block Cesium's web workers, which is
recorded as an expected failure below.

A page passes once the viewer reports it zoomed to the document: that needs
the geometry Cesium builds in web workers, which fail silently when broken.
"""

import http.server
import json
import os
import shutil
import socket
import subprocess
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from czml3 import CZML_VERSION, Document, Packet, Point, Polyline, Position
from czml3.properties import PositionList

_CANDIDATES = [
    os.environ.get("CZML3_BROWSER"),
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
    shutil.which("chrome"),
    shutil.which("msedge"),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
BROWSER = next((c for c in _CANDIDATES if c and Path(c).is_file()), None)


def _online(host: str = "cesium.com") -> bool:
    try:
        socket.create_connection((host, 443), timeout=5).close()
    except OSError:
        return False
    return True


pytestmark = [
    pytest.mark.browser,
    pytest.mark.skipif(BROWSER is None, reason="no Chrome/Chromium/Edge found"),
    pytest.mark.skipif(not _online(), reason="cesium.com is unreachable"),
]

DOC = Document(
    packets=[
        Packet(id="document", name="browser test", version=CZML_VERSION),
        Packet(
            id="a",
            position=Position(cartographicDegrees=[34.8, 32.1, 0]),
            point=Point(pixelSize=10),
        ),
        Packet(
            id="b",
            position=Position(cartographicDegrees=[35.2, 31.8, 0]),
            point=Point(pixelSize=10),
        ),
        Packet(
            id="link",
            polyline=Polyline(
                positions=PositionList(references=["a#position", "b#position"])
            ),
        ),
    ]
)
ENTITIES = 3  # the "document" packet configures the scene and is not an entity
# The viewer zooms to the document once its geometry is built, which needs
# Cesium's web workers (the polyline is built in one).
LOADED = {"entities": str(ENTITIES), "zoomed": "true", "globe": "loaded"}

# Relays the status the embedded viewer posts (see czml3._html) to the test
# server, so the test can wait in real time for the geometry to be built.
RELAY_TPL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin: 0">
{frame}
<script>
const status = {{}};
window.addEventListener("message", (event) => {{
    Object.assign(status, event.data.czml3 || {{}});
    fetch("{status_url}", {{ method: "POST", mode: "no-cors", body: JSON.stringify(status) }});
}});
</script>
</body></html>
"""
FRAME = '<iframe src="scene.html" style="width: 100%; height: 400px; border: none;"></iframe>'


class Site:
    """``tmp_path`` served on localhost, with an endpoint for the relayed status."""

    def __init__(self, root: Path) -> None:
        self.status: dict[str, str] = {}
        self._changed = threading.Condition()
        site = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, directory=str(root), **kwargs)

            def do_POST(self) -> None:
                body = self.rfile.read(int(self.headers["Content-Length"]))
                with site._changed:
                    site.status = {
                        key.removeprefix("czml3").lower(): value
                        for key, value in json.loads(body).items()
                    }
                    site._changed.notify_all()
                self.send_response(204)
                self.end_headers()

            def log_message(self, format: str, *args: Any) -> None:
                pass

        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

    def relay_page(self, frame: str) -> str:
        return RELAY_TPL.format(frame=frame, status_url=f"{self.url}/status")

    def wait_for_status(self, timeout: float) -> dict[str, str]:
        """Wait until the viewer loaded or failed, or ``timeout`` seconds passed."""
        with self._changed:
            self._changed.wait_for(
                lambda: LOADED.keys() <= self.status.keys() or "error" in self.status,
                timeout,
            )
            return dict(self.status)

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()


@pytest.fixture
def site(tmp_path: Path) -> Iterator[Site]:
    site = Site(tmp_path)
    try:
        yield site
    finally:
        site.close()


def _render(url: str, site: Site, profile: Path, timeout: float = 90) -> dict[str, str]:
    """Open ``url`` in headless Chrome and return the status relayed from it."""
    assert BROWSER is not None
    browser = subprocess.Popen(
        [
            BROWSER,
            "--headless=new",
            "--no-first-run",
            "--disable-extensions",
            # Software WebGL, so no GPU is needed.
            "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader",
            f"--user-data-dir={profile}",
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        return site.wait_for_status(timeout)
    finally:
        browser.terminate()
        browser.wait(timeout=30)


def test_standalone_page_renders_the_document(tmp_path: Path, site: Site) -> None:
    DOC.save_html(tmp_path / "scene.html")
    (tmp_path / "index.html").write_text(site.relay_page(FRAME), encoding="utf-8")

    assert _render(f"{site.url}/index.html", site, tmp_path / "profile") == LOADED


def test_jupyter_iframe_renders_the_document(tmp_path: Path, site: Site) -> None:
    (tmp_path / "notebook.html").write_text(
        site.relay_page(DOC._repr_html_()), encoding="utf-8"
    )

    assert _render(f"{site.url}/notebook.html", site, tmp_path / "profile") == LOADED


@pytest.mark.xfail(
    strict=True,
    reason="browsers block Cesium's web workers on file:// pages; serve the page over HTTP",
)
def test_standalone_page_opened_from_file(tmp_path: Path, site: Site) -> None:
    DOC.save_html(tmp_path / "scene.html")
    page = tmp_path / "index.html"
    page.write_text(site.relay_page(FRAME), encoding="utf-8")

    status = _render(page.resolve().as_uri(), site, tmp_path / "profile", timeout=30)

    assert status == LOADED
