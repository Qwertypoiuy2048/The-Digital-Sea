"""Pure calculations for the currently active program configuration."""

from __future__ import annotations

import constants


def _first_program(player):
    """Return the first editable program while supporting both save formats."""
    configured_programs = player.get("program", {})
    if isinstance(configured_programs, list):
        return configured_programs[0] if configured_programs and isinstance(configured_programs[0], dict) else None
    if isinstance(configured_programs, dict):
        return configured_programs
    return None


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


def _scaled_extension_cost(base_cost, frequency):
    """Scale a medium-tier extension cost for the module's current tier."""
    base_cost = _as_number(base_cost)
    if frequency == "high":
        return base_cost * 2
    if frequency in ("low", "below-minimum"):
        return max(1, base_cost // 2)
    return base_cost


def build_program_runtime(player, module_catalog, resource_capacity=None, cached_modules=None):
    """Resolve active modules and calculate current usage without mutating saves."""
    configured_programs = player.get("program", {})
    if isinstance(configured_programs, list):
        program_instances = [item for item in configured_programs if isinstance(item, dict)]
        program = program_instances[0] if program_instances else {}
    elif isinstance(configured_programs, dict):
        program_instances = [configured_programs] if configured_programs else []
        program = configured_programs
    else:
        program_instances = []
        program = {}
    active_modules = program.get("modules", {})
    if isinstance(active_modules, list):
        module_instances = [
            module for module in active_modules if isinstance(module, dict)
        ]
    elif isinstance(active_modules, dict):
        # Preserve compatibility with the earlier {"scan": 8} format.
        module_instances = [
            {"instanceId": module_id, "definitionId": module_id, "compute": allocation}
            for module_id, allocation in active_modules.items()
        ]
    else:
        module_instances = []
    configured_extensions = program.get("activeExtensions", [])
    if isinstance(configured_extensions, dict):
        extensions_are_mapped = True
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
        extensions_are_mapped = False
        extensions_by_module = {}
        active_extension_ids = configured_extensions
    else:
        extensions_are_mapped = True
        extensions_by_module = {}
        active_extension_ids = []

    definitions = module_catalog.get("modules", {})
    extension_definitions = module_catalog.get("extensions", {})
    modules = []
    assigned_extensions = []
    compute_used = 0
    warnings = []
    compile_state = program.get("compile", {}).get("state", "unknown")

    for module_instance in module_instances:
        instance_id = module_instance.get("instanceId", module_instance.get("definitionId", "unknown"))
        module_id = module_instance.get("definitionId", module_instance.get("id", instance_id))
        definition = definitions.get(module_id, {})
        allocation_value = module_instance.get("compute", module_instance.get("allocation", 0))
        allocation = _as_number(allocation_value)
        frequency = _frequency(definition, allocation)
        required_types = definition.get("necessaryExtensions", [])
        optional_types = definition.get("optionalExtensions", [])
        compatible_types = set(required_types + optional_types)
        candidate_extension_ids = (
            extensions_by_module.get(instance_id, [])
            if extensions_are_mapped else active_extension_ids
        )
        attached = []
        for extension_id in candidate_extension_ids:
            extension_type = extension_definitions.get(extension_id, {}).get("type")
            if extension_type in compatible_types:
                if extension_id not in attached:
                    attached.append(extension_id)
                    assigned_extensions.append(extension_id)

        missing_types = [
            extension_type for extension_type in required_types
            if not any(
                extension_definitions.get(extension_id, {}).get("type") == extension_type
                for extension_id in attached
            )
        ]
        extension_costs = {
            extension_id: _scaled_extension_cost(
                extension_definitions[extension_id].get("computeCost"), frequency
            )
            for extension_id in attached
            if extension_id in extension_definitions
        }
        extension_cost = sum(extension_costs.values())
        total_cost = allocation + extension_cost
        compute_used += total_cost
        module_size = _as_number(definition.get("size"))
        extension_size = sum(
            _as_number(extension_definitions[extension_id].get("size"))
            for extension_id in attached
            if extension_id in extension_definitions
        )
        if missing_types:
            warnings.append(f"{module_id} missing: {', '.join(missing_types)}")

        modules.append({
            "id": module_id,
            "instanceId": instance_id,
            "definitionId": module_id,
            "name": definition.get("name", module_id.replace("-", " ").title()),
            "allocation": allocation,
            "frequency": frequency,
            "minimumCompute": _as_number(definition.get("lowCompute")),
            "maximumCompute": _as_number(definition.get("highCompute")),
            "extensions": attached,
            "extensionCosts": extension_costs,
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
    program_instance_count = len(program_instances)
    cached_memory_used = 0
    cached_modules = cached_modules or {}
    for module_id in cached_modules.get("modules", []):
        cached_memory_used += _as_number(definitions.get(module_id, {}).get("size"))
    for extension_id in cached_modules.get("extensions", []):
        cached_memory_used += _as_number(extension_definitions.get(extension_id, {}).get("size"))
    return {
        "modules": modules,
        "extensions": active_extension_ids,
        "compute": {
            "used": compute_used,
            "capacity": capacity.get("compute"),
            "available": capacity.get("compute", 0) - compute_used,
        },
        "memory": {
            "used": cached_memory_used,
            "capacity": capacity.get("memory"),
            "available": capacity.get("memory", 0) - cached_memory_used,
        },
        "cores": {
            "used": program_instance_count,
            "capacity": capacity.get("cores"),
            "available": capacity.get("cores", 0) - program_instance_count,
        },
        "capacity": capacity,
        "compile": program.get("compile", {}),
        "warnings": warnings,
    }


def remove_module_instance(player, instance_id):
    """Remove one module instance and its instance-specific extensions in memory."""
    program = _first_program(player)
    if program is None:
        return False
    modules = program.get("modules", [])
    if not isinstance(modules, list):
        return False

    remaining_modules = [
        module for module in modules
        if module.get("instanceId") != instance_id
    ]
    removed = len(remaining_modules) != len(modules)
    if not removed:
        return False

    program["modules"] = remaining_modules
    active_extensions = program.get("activeExtensions")
    if isinstance(active_extensions, dict):
        active_extensions.pop(instance_id, None)
    return True


def remove_extension_from_instance(player, instance_id, extension_id):
    """Remove one extension from one module instance in memory."""
    program = _first_program(player)
    if program is None:
        return False
    active_extensions = program.get("activeExtensions")
    if isinstance(active_extensions, dict):
        extensions = active_extensions.get(instance_id, [])
        if extension_id not in extensions:
            return False
        active_extensions[instance_id] = [
            value for value in extensions if value != extension_id
        ]
        return True
    if isinstance(active_extensions, list) and extension_id in active_extensions:
        active_extensions.remove(extension_id)
        return True
    return False


def adjust_module_compute(player, module_catalog, instance_id, direction):
    """Move one module instance to its next lower or higher compute tier."""
    if module_compute_error(player, module_catalog, instance_id, direction):
        return False
    program = _first_program(player)
    if program is None or not isinstance(program.get("modules"), list):
        return False

    module = next((item for item in program["modules"]
                   if item.get("instanceId") == instance_id), None)
    if module is None:
        return False
    definition = module_catalog.get("modules", {}).get(module.get("definitionId"), {})
    tiers = [
        int(definition[key]) for key in ("lowCompute", "mediumCompute", "highCompute")
        if key in definition
    ]
    tiers = sorted(set(tiers))
    if not tiers:
        return False

    current = _as_number(module.get("compute"))
    if direction > 0:
        next_values = [value for value in tiers if value > current]
        if not next_values:
            return False
        module["compute"] = next_values[0]
    else:
        previous_values = [value for value in tiers if value < current]
        if not previous_values:
            return False
        module["compute"] = previous_values[-1]
    return True


def module_compute_error(player, module_catalog, instance_id, direction):
    """Return a reason when a module cannot move to its next compute tier."""
    program = _first_program(player)
    if program is None or not isinstance(program.get("modules"), list):
        return "No editable module is available."
    module = next((item for item in program["modules"]
                   if item.get("instanceId") == instance_id), None)
    if module is None:
        return "Module instance was not found."
    definition = module_catalog.get("modules", {}).get(module.get("definitionId"), {})
    tiers = sorted({
        _as_number(definition[key]) for key in ("lowCompute", "mediumCompute", "highCompute")
        if key in definition
    })
    current = _as_number(module.get("compute"))
    candidates = [value for value in tiers if value > current] if direction > 0 else [
        value for value in tiers if value < current
    ]
    if not candidates:
        return "Already at the highest compute tier." if direction > 0 else "Already at the lowest compute tier."
    next_compute = candidates[0] if direction > 0 else candidates[-1]
    runtime = build_program_runtime(player, module_catalog)
    runtime_module = next(item for item in runtime["modules"] if item["instanceId"] == instance_id)
    next_frequency = _frequency(definition, next_compute)
    extension_cost = sum(
        _scaled_extension_cost(
            module_catalog.get("extensions", {}).get(extension_id, {}).get("computeCost"),
            next_frequency,
        )
        for extension_id in runtime_module["extensions"]
    )
    next_total = next_compute + extension_cost
    delta = next_total - runtime_module["computeCost"]
    if direction > 0 and delta > runtime["compute"]["available"]:
        return f"Needs {delta} additional CU, but only {runtime['compute']['available']} CU is available."
    return None


def module_add_error(player, module_catalog, cached_modules, definition_id):
    """Return a user-facing reason when a cached module cannot be added."""
    if definition_id not in cached_modules.get("modules", []):
        return "Module is not available in the code cache."
    definition = module_catalog.get("modules", {}).get(definition_id)
    if definition is None:
        return "Module definition is missing."
    program = _first_program(player)
    if program is None:
        return "No editable program instance is available."
    modules = program.get("modules", [])
    if not isinstance(modules, list):
        return "Program module data is invalid."
    matching = [module for module in modules
                if module.get("definitionId") == definition_id]
    if not definition.get("replicable", True) and matching:
        return "This module cannot be duplicated."
    max_instances = definition.get("maxInstances")
    if max_instances is not None and len(matching) >= _as_number(max_instances):
        return "Maximum module instances reached."

    runtime = build_program_runtime(player, module_catalog, cached_modules=cached_modules)
    compute_cost = _as_number(definition.get("mediumCompute"), _as_number(definition.get("lowCompute")))
    if runtime["compute"]["available"] < compute_cost:
        return f"Needs {compute_cost} CU, but only {runtime['compute']['available']} CU is available."
    return None


def add_module_instance(player, module_catalog, cached_modules, definition_id):
    """Add a new medium-tier module instance to the first program."""
    error = module_add_error(player, module_catalog, cached_modules, definition_id)
    if error:
        return None
    program = _first_program(player)
    modules = program["modules"]
    prefix = f"{definition_id}-"
    used_numbers = []
    for module in modules:
        instance_id = str(module.get("instanceId", ""))
        if instance_id.startswith(prefix):
            suffix = instance_id[len(prefix):]
            if suffix.isdigit():
                used_numbers.append(int(suffix))
    next_number = max(used_numbers, default=0) + 1
    instance_id = f"{prefix}{next_number:02d}"
    definition = module_catalog["modules"][definition_id]
    modules.append({
        "instanceId": instance_id,
        "definitionId": definition_id,
        "compute": _as_number(definition.get("mediumCompute"),
                               _as_number(definition.get("lowCompute"))),
    })
    active_extensions = program.setdefault("activeExtensions", {})
    if isinstance(active_extensions, dict):
        active_extensions.setdefault(instance_id, [])
    return instance_id


def extension_add_error(player, module_catalog, cached_modules, instance_id, extension_id):
    """Return a user-facing reason when an extension cannot be attached."""
    if extension_id not in cached_modules.get("extensions", []):
        return "Extension is not available in the code cache."
    program = _first_program(player)
    if program is None:
        return "No editable program instance is available."
    module = next((item for item in program.get("modules", [])
                   if item.get("instanceId") == instance_id), None)
    if module is None:
        return "Module instance was not found."
    extension = module_catalog.get("extensions", {}).get(extension_id)
    definition = module_catalog.get("modules", {}).get(module.get("definitionId"), {})
    if extension is None:
        return "Extension definition is missing."
    compatible_types = set(definition.get("necessaryExtensions", []) +
                           definition.get("optionalExtensions", []))
    if extension.get("type") not in compatible_types:
        return "This extension is incompatible with the selected module."
    active_extensions = program.get("activeExtensions", {})
    attached = active_extensions.get(instance_id, []) if isinstance(active_extensions, dict) else []
    if extension_id in attached:
        return "This extension is already attached."
    runtime = build_program_runtime(player, module_catalog)
    runtime_module = next(item for item in runtime["modules"] if item["instanceId"] == instance_id)
    extension_cost = _scaled_extension_cost(extension.get("computeCost"), runtime_module["frequency"])
    if extension_cost > runtime["compute"]["available"]:
        return f"Needs {extension_cost} CU, but only {runtime['compute']['available']} CU is available."
    return None


def add_extension_to_instance(player, module_catalog, cached_modules, instance_id, extension_id):
    """Attach one cached extension to one module instance in memory."""
    if extension_add_error(player, module_catalog, cached_modules, instance_id, extension_id):
        return False
    program = _first_program(player)
    active_extensions = program.setdefault("activeExtensions", {})
    if not isinstance(active_extensions, dict):
        return False
    active_extensions.setdefault(instance_id, []).append(extension_id)
    return True
