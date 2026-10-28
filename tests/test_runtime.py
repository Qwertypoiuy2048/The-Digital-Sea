import copy
import unittest

import constants
from data_loader import load_json
from program_runtime import (
    _as_number,
    _frequency,
    _scaled_extension_cost,
    add_extension_to_instance,
    add_module_instance,
    adjust_module_compute,
    build_program_runtime,
    extension_add_error,
    module_add_error,
    module_compute_error,
    remove_extension_from_instance,
    remove_module_instance,
)


class RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_json("modules.json")
        cls.cached = load_json("cached_modules.json")
        cls.player_fixture = load_json("player.json")

    def player(self):
        return copy.deepcopy(self.player_fixture)

    def test_shipped_data_loads_with_expected_top_level_shape(self):
        self.assertIn("program", self.player_fixture)
        self.assertIn("modules", self.catalog)
        self.assertIn("extensions", self.catalog)
        self.assertIsInstance(self.cached["modules"], list)
        self.assertIsInstance(self.cached["extensions"], list)

    def test_number_and_frequency_helpers_handle_bad_values(self):
        self.assertEqual(_as_number("12"), 12)
        self.assertEqual(_as_number("bad", 7), 7)
        definition = {"lowCompute": 4, "mediumCompute": 8, "highCompute": 16}
        self.assertEqual(_frequency(definition, 3), "below-minimum")
        self.assertEqual(_frequency(definition, 4), "low")
        self.assertEqual(_frequency(definition, 8), "medium")
        self.assertEqual(_frequency(definition, 16), "high")
        self.assertEqual(_scaled_extension_cost(5, "high"), 10)
        self.assertEqual(_scaled_extension_cost(5, "medium"), 5)
        self.assertEqual(_scaled_extension_cost(5, "low"), 2)
        self.assertEqual(_scaled_extension_cost(0, "low"), 1)

    def test_shipped_runtime_is_complete_and_within_expected_resources(self):
        runtime = build_program_runtime(self.player_fixture, self.catalog, cached_modules=self.cached)
        self.assertEqual(len(runtime["modules"]), 8)
        self.assertEqual(runtime["compute"]["used"], 166)
        self.assertEqual(runtime["compute"]["available"], 90)
        self.assertEqual(runtime["memory"]["used"], 132)
        self.assertEqual(runtime["cores"]["used"], 1)
        self.assertEqual(runtime["compile"]["state"], "finished")
        self.assertFalse(runtime["warnings"])

    def test_runtime_does_not_mutate_player(self):
        player = self.player()
        original = copy.deepcopy(player)
        build_program_runtime(player, self.catalog, self.cached)
        self.assertEqual(player, original)

    def test_runtime_supports_legacy_dict_module_format(self):
        player = {"program": {"modules": {"scan": 8}, "compile": {"state": "clean"}}}
        runtime = build_program_runtime(player, self.catalog)
        self.assertEqual(runtime["modules"][0]["instanceId"], "scan")
        self.assertEqual(runtime["modules"][0]["allocation"], 8)

    def test_runtime_supports_empty_and_malformed_program_containers(self):
        for value in (None, [], "invalid", 42):
            runtime = build_program_runtime({"program": value}, self.catalog)
            self.assertEqual(runtime["modules"], [])
            self.assertEqual(runtime["cores"]["used"], 0)

    def test_missing_required_extension_blocks_module_and_warns(self):
        player = self.player()
        program = player["program"][0]
        program["activeExtensions"]["signal-disrupter-01"] = []
        runtime = build_program_runtime(player, self.catalog)
        module = next(m for m in runtime["modules"] if m["instanceId"] == "signal-disrupter-01")
        self.assertEqual(module["state"], "blocked")
        self.assertEqual(module["missingExtensions"], ["combatType"])
        self.assertTrue(any("signal-disrupter" in warning for warning in runtime["warnings"]))

    def test_unattached_extension_warns(self):
        player = self.player()
        player["program"][0]["activeExtensions"]["unknown-module"] = ["dual-thread-schedule"]
        runtime = build_program_runtime(player, self.catalog)
        self.assertTrue(any("unattached extensions" in warning for warning in runtime["warnings"]))

    def test_cached_memory_counts_known_modules_and_extensions(self):
        runtime = build_program_runtime(
            {"program": []}, self.catalog,
            cached_modules={"modules": ["scan", "missing"], "extensions": ["defrag-patch", "missing"]},
        )
        self.assertEqual(runtime["memory"]["used"], 18)

    def test_remove_module_removes_its_mapped_extensions(self):
        player = self.player()
        self.assertTrue(remove_module_instance(player, "scan-01"))
        program = player["program"][0]
        self.assertNotIn("scan-01", [m["instanceId"] for m in program["modules"]])
        self.assertNotIn("scan-01", program["activeExtensions"])
        self.assertFalse(remove_module_instance(player, "scan-01"))

    def test_remove_module_rejects_legacy_dict_modules(self):
        player = {"program": {"modules": {"scan": 8}}}
        self.assertFalse(remove_module_instance(player, "scan"))

    def test_remove_extension_works_for_mapped_and_flat_formats(self):
        player = self.player()
        self.assertTrue(remove_extension_from_instance(player, "scan-01", "passive-scan"))
        self.assertNotIn("passive-scan", player["program"][0]["activeExtensions"]["scan-01"])
        flat = {"program": {"activeExtensions": ["x", "y"]}}
        self.assertTrue(remove_extension_from_instance(flat, "ignored", "x"))
        self.assertEqual(flat["program"]["activeExtensions"], ["y"])

    def test_compute_adjustment_moves_through_sorted_tiers(self):
        player = self.player()
        self.assertTrue(adjust_module_compute(player, self.catalog, "scan-01", 1))
        self.assertEqual(player["program"][0]["modules"][0]["compute"], 16)
        self.assertTrue(adjust_module_compute(player, self.catalog, "scan-01", -1))
        self.assertEqual(player["program"][0]["modules"][0]["compute"], 8)
        self.assertTrue(adjust_module_compute(player, self.catalog, "scan-01", -1))
        self.assertEqual(player["program"][0]["modules"][0]["compute"], 4)
        self.assertFalse(adjust_module_compute(player, self.catalog, "scan-01", -1))

    def test_compute_error_reports_missing_module_and_tier_limits(self):
        player = self.player()
        self.assertEqual(module_compute_error(player, self.catalog, "missing", 1), "Module instance was not found.")
        player["program"][0]["modules"][0]["compute"] = 16
        self.assertEqual(module_compute_error(player, self.catalog, "scan-01", 1), "Already at the highest compute tier.")

    def test_add_module_checks_cache_replicability_and_capacity(self):
        player = self.player()
        self.assertEqual(module_add_error(player, self.catalog, self.cached, "scan"), "This module cannot be duplicated.")
        self.assertIsNone(module_add_error(player, self.catalog, self.cached, "kernel-threader"))
        instance_id = add_module_instance(player, self.catalog, self.cached, "kernel-threader")
        self.assertEqual(instance_id, "kernel-threader-01")
        self.assertIn(instance_id, player["program"][0]["activeExtensions"])
        self.assertEqual(add_module_instance(player, self.catalog, self.cached, "not-cached"), None)

    def test_add_module_uses_next_available_instance_number(self):
        player = {"program": [{"modules": [{"instanceId": "data-harvester-01", "definitionId": "data-harvester", "compute": 12}], "activeExtensions": {}}]}
        instance_id = add_module_instance(player, self.catalog, self.cached, "data-harvester")
        self.assertEqual(instance_id, "data-harvester-02")

    def test_extension_add_checks_cache_compatibility_duplicates_and_success(self):
        player = self.player()
        self.assertEqual(extension_add_error(player, self.catalog, self.cached, "scan-01", "firewall-daemon"), "This extension is incompatible with the selected module.")
        self.assertEqual(extension_add_error(player, self.catalog, self.cached, "scan-01", "security-scan"), "This extension is already attached.")
        player["program"][0]["modules"].append({"instanceId": "kernel-threader-01", "definitionId": "kernel-threader", "compute": 6})
        self.assertIsNone(extension_add_error(player, self.catalog, self.cached, "kernel-threader-01", "dual-thread-schedule"))
        self.assertTrue(add_extension_to_instance(player, self.catalog, self.cached, "kernel-threader-01", "dual-thread-schedule"))

    def test_missing_program_and_definitions_return_user_errors(self):
        empty = {"program": []}
        self.assertEqual(module_add_error(empty, self.catalog, self.cached, "scan"), "No editable program instance is available.")
        self.assertEqual(extension_add_error(empty, self.catalog, self.cached, "scan-01", "security-scan"), "No editable program instance is available.")
        player = self.player()
        self.assertEqual(extension_add_error(player, {"modules": {}, "extensions": {}}, self.cached, "scan-01", "security-scan"), "Extension definition is missing.")


if __name__ == "__main__":
    unittest.main()
