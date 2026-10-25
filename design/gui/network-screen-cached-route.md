# Network Screen — Cached Route State

## Purpose

This is a second state of the fullscreen 9:16 Network screen. The player has accumulated more cached information and can now see a dense group of cached devices branching from a scanned connection on the primary device.

The screen demonstrates route planning rather than a separate selection mode. The safe route is highlighted from primary node 3 to secondary node 1. It does not pass through any locked or monitored connection.

## Source mockup

- SVG: `network-screen-cached-route.svg`
- ViewBox: `720 x 1280`
- Orientation: portrait, 9:16
- Intended presentation: fullscreen

## Primary active device

ID: `primary-active-device` (visual group can be added around the primary device implementation)

The primary device has four scanned connections:

| Node | Strength | State | Visual treatment | Route use |
|---|---|---|---|---|
| Primary node 1 | Strong | Locked | Thick cyan line plus red lock | Cannot pass through |
| Primary node 2 | Weak | Locked | Thin muted line plus red lock | Cannot pass through |
| Primary node 3 | Weak | Unstable | Thin dashed amber line | Route origin |
| Primary node 4 | Strong | Monitored | Thick purple line plus purple `!` | Avoid; monitored |

The primary node 3 connection is the only route used to reach the cached network in this mockup.

## Cached network

The mockup shows twelve cached devices, providing more than the requested 5–8 device range to make the branching network readable:

- Main route devices: `cached-device-1` through `cached-device-6`
- Branch devices: `cached-device-branch-a` through `cached-device-branch-f`

Each cached device is ghosted, desaturated, and non-pulsing. Cached devices vary in size to communicate their scanned capacity. The cached network includes 2–5 connections per node across its main route and branches.

Cached connection IDs:

- `cache-connection-1-2`
- `cache-connection-1-branch`
- `cache-connection-2-3`
- `cache-connection-2-branch`
- `cache-connection-3-4`
- `cache-connection-3-branch`
- `cache-connection-4-5`
- `cache-connection-4-branch`
- `cache-connection-5-6`
- `cache-connection-5-branch`
- `cache-connection-6-secondary`
- `cache-connection-6-branch`

## Secondary active device

The secondary active device is `secondary-active-device`. It has three scanned connections:

| Node | Strength | State | Visual treatment | Route use |
|---|---|---|---|---|
| Secondary node 1 | Strong | Open | Thick cyan line | Route endpoint |
| Secondary node 2 | Strong | Monitored + locked | Thick purple line, purple `!`, red lock | Cannot pass through |
| Secondary node 3 | Weak | Open | Thin muted line | Available but not used |

The route reaches secondary node 1 through `secondary-node-1-connection`.

## Route rules

The highlighted route is represented by:

- `safe-route-glow`
- `safe-route-core`

The route begins at primary node 3, follows the cached main chain, and ends at secondary node 1:

`primary-node-3-connection` → `cached-device-1` → `cached-device-2` → `cached-device-3` → `cached-device-4` → `cached-device-5` → `cached-device-6` → `secondary-node-1-connection`

The route must not traverse:

- Any connection with a lock marker
- Any monitored connection with a purple hue and `!` marker

The implementation should validate route candidates against connection metadata rather than relying only on the visual highlight.

## Connection visual encoding

- Strong bandwidth: thick line
- Weak bandwidth: thin line
- Stable: solid line
- Unstable: dashed line
- Locked: red lock marker
- Monitored: purple line or hue with purple `!` marker
- Safe route: bright cyan/sea-green glow and core line

These encodings are intentionally redundant so route legality is understandable by color, shape, and direct markers.

## Stable element IDs

### Active devices

- `secondary-active-device`
- Add a wrapper ID of `primary-active-device` when integrating the primary device into a scene component.

### Cached devices

- `cached-device-1` through `cached-device-6`
- `cached-device-branch-a` through `cached-device-branch-f`
- `cached-devices`

### Primary connections

- `primary-node-1-connection`
- `primary-node-2-connection`
- `primary-node-3-connection`
- `primary-node-4-connection`

### Secondary connections

- `secondary-node-1-connection`
- `secondary-node-2-connection`
- `secondary-node-3-connection`

### Status markers

- `lock-primary-node-1`
- `lock-primary-node-2`
- `lock-secondary-node-2`
- `monitor-primary-node-4`
- `monitor-secondary-node-2`

### Route and readout

- `safe-route`
- `safe-route-glow`
- `safe-route-core`
- `scan-labels`
