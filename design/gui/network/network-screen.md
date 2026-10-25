# Network Screen

## Purpose

The Network screen is a fullscreen, zoomable map of the player program's known network space. It centers on the player's current devices and combines currently visible connections with cached information from earlier scans.

The first version is intentionally direct: it shows device size, connection bandwidth, connection stability, and connection security status when the active scan can determine them. A persistent legend is intentionally omitted; visual meaning should be learned from direct labels and scan feedback first.

## Source mockup

- SVG: `network-screen.svg`
- ViewBox: `720 x 1280`
- Orientation: portrait, 9:16
- Intended presentation: fullscreen
- Map interaction: zoom and pan; selecting an object is part of scanning/inspection rather than a separate selection mode

## Visual rules

### Active player devices

Player devices use the main player color, bright glow, and a strong outline.

- `player-device-primary-a`: main program device, largest primary node
- `player-device-primary-b`: second primary node, closely connected to A
- `player-device-secondary`: active but non-primary device, dimmer player color

The two primary devices work together to run the main program and therefore have a strong, thick connection between them. The secondary device remains active but is visually subordinate.

Device size is the only device specification shown in the basic network view. Larger nodes represent larger capacity according to the current scan interpretation.

### Cached devices

Cached devices represent stored information rather than currently confirmed live visibility.

They use:

- Reduced opacity
- Desaturated color
- No active pulse
- A small `C` cached-data marker

Cached nodes should not be mistaken for active devices. Their appearance may become more detailed when a new scan confirms or updates them.

### Connections

- Bandwidth is represented by line thickness.
- Stable connections use solid lines.
- Unstable connections use dashed lines.
- Security is represented by a scan-return marker or status indicator. The initial SVG uses direct connection state and leaves room for a pass/fail marker to be added by the implementation.
- Visible connections may carry pulses to suggest data flow.
- Cached connection traces are ghosted and do not pulse.

The primary A-to-B connection is the strongest visible connection. The secondary device has a weaker visible link, and its outward unstable connection is dashed.

## Scan-dependent information

The map should not invent details the player has not discovered. Each object has a knowledge state supplied by the player's active scans and stored information.

Suggested knowledge states:

- `unknown`: not rendered or rendered as a vague signal
- `cached`: ghosted node/trace with cached marker
- `visible-basic`: current device/connection visible with basic properties
- `inspected`: additional scan-return data available in an inspection view
- `stale`: cached data exists but may no longer be accurate

The active upgrade set controls which fields a scan can return. Stored information can reveal details even when the object is not currently visible, but those details should be marked as cached or stale.

## Stable element IDs

### Background and atmosphere

- `network-background`
- `network-current-field`

### Active devices

- `player-device-primary-a`
- `player-device-primary-b`
- `player-device-secondary`
- `active-player-devices`

### Cached devices

- `cached-device-north`
- `cached-device-east`
- `cached-device-south`
- `cached-devices`

### Connections

- `connection-main-cluster`
- `connection-main-cluster-core`
- `connection-main-to-third`
- `connection-third-unstable`
- `connection-cache-visible`
- `connection-cache-north`
- `connection-cache-east`
- `connection-cache-south`
- `connection-pulses`

### Readout

- `scan-status`
- `device-labels`

## Future interaction states

The first mockup does not add a persistent legend or large detail panel. Later states can add contextual scan readouts for:

- Selected device specifications
- Connection bandwidth/stability/security results
- Cached-data age and confidence
- Available actions such as inspect, route, copy, seed backup, or sever connection

These should appear as scan results and contextual overlays rather than as permanent HUD clutter.
