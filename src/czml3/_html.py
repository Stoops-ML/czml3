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
// Load status is recorded on <body> as data-czml3-entities, data-czml3-zoomed
// (set once the document's geometry is built), data-czml3-globe (set once the
// first globe tiles have loaded) and data-czml3-error (the latest error, including
// failed imagery tiles), and posted to the embedding page when shown in an iframe
// (e.g. Jupyter).
const reportStatus = (key, value) => {{
    document.body.dataset[key] = value;
    if (window.parent !== window) {{
        window.parent.postMessage({{ czml3: {{ [key]: value }} }}, "*");
    }}
}};
const reportError = (error) => reportStatus("czml3Error", String(error));
window.addEventListener("error", (event) => reportError(event.message));
// In an <iframe srcdoc> (e.g. Jupyter) the page URL is about:srcdoc, so CesiumJS
// mistakes its worker modules for cross-origin URLs and starts each worker with
// a bare `import "createGeometry";`, which cannot load: no globe or worker-built
// geometry is drawn, and no error is raised. Import the worker's full URL instead.
if (location.protocol === "about:") {{
    const NativeBlob = window.Blob;
    window.Blob = class extends NativeBlob {{
        constructor(parts, options) {{
            const bareImport = parts && parts.length === 1 && typeof parts[0] === "string"
                && /^import "([\\w-]+)";$/.exec(parts[0]);
            if (bareImport) {{
                const url = Cesium.buildModuleUrl("Workers/" + bareImport[1] + ".js");
                parts = ["import " + JSON.stringify(url) + ";"];
            }}
            super(parts, options);
        }}
    }};
}}
const czml = {czml};
const ionToken = {ion_token};
const options = {{ shouldAnimate: true }};
if (ionToken) {{
    Cesium.Ion.defaultAccessToken = ionToken;
    options.terrain = Cesium.Terrain.fromWorldTerrain();
}} else {{
    // Without a Cesium ion token the default ion imagery is unavailable. Use the
    // low-resolution Natural Earth II imagery shipped with CesiumJS: third-party
    // tile servers such as OpenStreetMap's can refuse requests from notebook
    // frames (e.g. VS Code's).
    options.baseLayer = Cesium.ImageryLayer.fromProviderAsync(
        Cesium.TileMapServiceImageryProvider.fromUrl(
            Cesium.buildModuleUrl("Assets/Textures/NaturalEarthII")
        )
    );
    options.baseLayer.errorEvent.addEventListener(reportError);
    options.baseLayer.readyEvent.addEventListener((provider) => {{
        provider.errorEvent.addEventListener((error) => reportError(error.message));
    }});
}}
const viewer = new Cesium.Viewer("cesiumContainer", options);
viewer.scene.renderError.addEventListener((scene, error) => reportError(error));
viewer.scene.globe.tileLoadProgressEvent.addEventListener((queued) => {{
    if (queued === 0) reportStatus("czml3Globe", "loaded");
}});
Cesium.CzmlDataSource.load(czml).then((dataSource) => {{
    viewer.dataSources.add(dataSource);
    reportStatus("czml3Entities", String(dataSource.entities.values.length));
    return viewer.zoomTo(dataSource);
}}).then((zoomed) => reportStatus("czml3Zoomed", String(zoomed))).catch(reportError);
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
    """Embed a standalone page in an iframe, e.g. for Jupyter output.

    The iframe keeps the viewer's CSS and globals apart from the host page, but
    it is deliberately not sandboxed: in a sandboxed (opaque-origin) frame the
    browser blocks CesiumJS's web workers, so no worker-built geometry
    (polylines, polygons, boxes, ...) is drawn.
    """
    return (
        f'<iframe srcdoc="{html.escape(page, quote=True)}" '
        f'style="width: 100%; height: {html.escape(height)}; border: none;">'
        "</iframe>"
    )
