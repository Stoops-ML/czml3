"""Standalone HTML previews of a CZML document, rendered with CesiumJS."""

from __future__ import annotations

import html
import json
from typing import Any

#: CesiumJS release loaded by default. The page uses the ``baseLayer`` and
#: ``terrain`` viewer options, which need CesiumJS 1.107 or later.
DEFAULT_CESIUM_VERSION = "1.145"

_CESIUM_URL = "https://cesium.com/downloads/cesiumjs/releases/{version}/Build/Cesium/"

_PAGE_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="{base_url}Cesium.js"></script>
<link rel="stylesheet" href="{base_url}Widgets/widgets.css">
<style>html, body, #cesiumContainer {{ width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden; }}</style>
</head>
<body>
<div id="cesiumContainer"></div>
<script>
// Load status is recorded on <body> as data-czml3-entities / data-czml3-error.
const reportError = (error) => {{ document.body.dataset.czml3Error = String(error); }};
window.addEventListener("error", (event) => reportError(event.message));
const czml = {czml};
const ionToken = {ion_token};
const options = {{ shouldAnimate: true }};
if (ionToken) {{
    Cesium.Ion.defaultAccessToken = ionToken;
    options.terrain = Cesium.Terrain.fromWorldTerrain();
}} else {{
    // Without a Cesium ion token the default ion imagery is unavailable.
    options.baseLayer = new Cesium.ImageryLayer(
        new Cesium.OpenStreetMapImageryProvider({{ url: "https://tile.openstreetmap.org/" }})
    );
}}
const viewer = new Cesium.Viewer("cesiumContainer", options);
viewer.scene.renderError.addEventListener((scene, error) => reportError(error));
Cesium.CzmlDataSource.load(czml).then((dataSource) => {{
    viewer.dataSources.add(dataSource);
    viewer.zoomTo(dataSource);
    document.body.dataset.czml3Entities = String(dataSource.entities.values.length);
}}).catch(reportError);
</script>
</body>
</html>
"""


def _script_literal(value: Any) -> str:
    """Serialize ``value`` as a JavaScript literal that is safe inside <script>.

    Escaping ``<`` stops a CZML string such as an HTML description containing
    ``</script>`` from ending the script element early.
    """
    return json.dumps(value).replace("<", "\\u003c")


def document_html(
    czml: Any,
    *,
    title: str,
    cesium_version: str = DEFAULT_CESIUM_VERSION,
    ion_token: str | None = None,
) -> str:
    """Return a standalone HTML page that displays ``czml`` in a Cesium viewer."""
    return _PAGE_TPL.format(
        title=html.escape(title),
        base_url=_CESIUM_URL.format(version=html.escape(cesium_version)),
        czml=_script_literal(czml),
        ion_token=_script_literal(ion_token or ""),
    )


def iframe_html(page: str, *, height: str = "400px") -> str:
    """Embed a standalone page in a sandboxed iframe, e.g. for Jupyter output."""
    return (
        f'<iframe srcdoc="{html.escape(page, quote=True)}" '
        f'style="width: 100%; height: {html.escape(height)}; border: none;" '
        'sandbox="allow-scripts"></iframe>'
    )
