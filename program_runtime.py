"""Pure calculations for the currently active program configuration."""

from __future__ import annotations

import constants


def _as_number(value, fallback=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _frequency(definition, allocation):
    tiers = (
        ("high", definition.get("highCompute")),
        ("medium", definition.get("mediumCompute")),
        ("low", definition.get("lowCompute")),
    )
    for name, threshold in tiers:
        if threshold is not None and allocation >= _as_number(threshold):
            return name
    return "below-minimum"


def build_program_runtime(player, module_catalog, resource_capacity=None):
    """Resolve active modules and calculate current usage without mutating saves."""
    program = player.get("program", {})
    active_modules = program.get("modules", {})
    if not isinstance(active_modules, dict):
        active_modules = {}
    configured_extensions = program.get("activeExtensions", [])
    if isinstance(configured_extensions, dict):
        extensions_by_module = {
            module_id: extension_ids
            for module_id, extension_ids in configured_extensions.items()
            if isinstance(extension_ids, list)
        }
        active_extension_ids = [
            extension_id
            for extension_ids in extensions_by_module.values()
            for extension_id in extension_ids
        ]
    elif isinstance(configured_extensions, list):
        extensions_by_module = {}
        active_extension_ids = configured_extensions
    else:
        extensions_by_module = {}
        active_extension_ids = []

    definitions = module_catalog.get("modules", {})
    extension_definitions = module_catalog.get("extensions", {})
    modules = []
    assigned_extensions = set()
    compute_used = 0
    memory_used = 0
    warnings = []
    compile_state = program.get("compile", {}).get("state", "unknown")

    for module_id, allocation_value in active_modules.items():
        definition = definitions.get(module_id, {})
        allocation = _as_number(allocation_value)
        required_types = definition.get("necessaryExtensions", [])
        optional_types = definition.get("optionalExtensions", [])
        compatible_types = set(required_types + optional_types)
        candidate_extension_ids = extensions_by_module.get(module_id, active_extension_ids)
        attached = []
        for extension_id in candidate_extension_ids:
            extension_type = extension_definitions.get(extension_id, {}).get("type")
            if extension_type in compatible_types:
                if extension_id not in assigned_extensions:
                    attached.append(extension_id)
                    assigned_extensions.add(extension_id)

        missing_types = [
            extension_type for extension_type in required_types
            if not any(
                extension_definitions.get(extension_id, {}).get("type") == extension_type
                for extension_id in attached
            )
        ]
        extension_cost = sum(
            _as_number(extension_definitions[extension_id].get("computeCost"))
            for extension_id in attached
            if extension_id in extension_definitions
        )
        total_cost = allocation + extension_cost
        compute_used += total_cost
        module_size = _as_number(definition.get("size"))
        extension_size = sum(
            _as_number(extension_definitions[extension_id].get("size"))
            for extension_id in attached
            if extension_id in extension_definitions
        )
        memory_used += module_size + extension_size
        if missing_types:
            warnings.append(f"{module_id} missing: {', '.join(missing_types)}")

        modules.append({
            "id": module_id,
            "name": definition.get("name", module_id.replace("-", " ").title()),
            "allocation": allocation,
            "frequency": _frequency(definition, allocation),
            "minimumCompute": _as_number(definition.get("lowCompute")),
            "maximumCompute": _as_number(definition.get("highCompute")),
            "extensions": attached,
            "extensionCost": extension_cost,
            "computeCost": total_cost,
            "memoryCost": module_size + extension_size,
            "details": list(definition.get("details", [])),
            "missingExtensions": missing_types,
            "state": "blocked" if missing_types else (
                "active" if compile_state in ("finished", "complete", "clean") else compile_state
            ),
            "automatic": definition.get("automatic", False),
            "cooldown": definition.get("cooldown"),
        })

    unassigned_extensions = [
        extension_id for extension_id in active_extension_ids
        if extension_id not in assigned_extensions
    ]
    if unassigned_extensions:
        warnings.append(f"unattached extensions: {', '.join(unassigned_extensions)}")

    capacity = dict(resource_capacity or constants.DEFAULT_DEVICE_RESOURCES)
    return {
        "modules": modules,
        "extensions": active_extension_ids,
        "compute": {
            "used": compute_used,
            "capacity": capacity.get("compute"),
            "available": capacity.get("compute", 0) - compute_used,
        },
        "memory": {
            "used": memory_used,
            "capacity": capacity.get("memory"),
            "available": capacity.get("memory", 0) - memory_used,
        },
        "capacity": capacity,
        "compile": program.get("compile", {}),
        "warnings": warnings,
    }
