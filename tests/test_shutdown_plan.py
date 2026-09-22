import unittest

from shutdown_plan import (
    MAX_DELAY_SECONDS,
    MIN_DELAY_SECONDS,
    create_plan,
    validate_delay,
    validate_target,
)


class ShutdownPlanTests(unittest.TestCase):
    def test_windows_plan_has_delay_and_abort_without_force(self):
        plan = create_plan("windows", "shutdown", "local", 300)
        self.assertIn("/t 300", plan.command)
        self.assertNotIn("/f", plan.command)
        self.assertEqual(plan.abort_command, "shutdown /a")

    def test_remote_windows_target_is_validated(self):
        plan = create_plan("windows", "restart", "host-01.example", 600)
        self.assertIn(r"/m \\host-01.example", plan.command)
        with self.assertRaises(ValueError):
            validate_target("host && whoami")

    def test_linux_remote_requires_safe_user(self):
        with self.assertRaises(ValueError):
            create_plan("linux", "shutdown", "10.0.0.5", 300)
        plan = create_plan("linux", "shutdown", "10.0.0.5", 300, "admin")
        self.assertIn("ssh admin@10.0.0.5 -- sudo shutdown -h +5", plan.command)
        self.assertIn("sudo shutdown -c", plan.abort_command)

    def test_delay_has_safe_bounds(self):
        self.assertEqual(validate_delay(MIN_DELAY_SECONDS), MIN_DELAY_SECONDS)
        self.assertEqual(validate_delay(MAX_DELAY_SECONDS), MAX_DELAY_SECONDS)
        with self.assertRaises(ValueError):
            validate_delay(0)
        with self.assertRaises(ValueError):
            validate_delay(MAX_DELAY_SECONDS + 1)

    def test_local_linux_restart_is_non_immediate(self):
        plan = create_plan("linux", "restart", "local", 60)
        self.assertEqual(plan.command, "sudo shutdown -r +1")
        self.assertEqual(plan.abort_command, "sudo shutdown -c")


if __name__ == "__main__":
    unittest.main()
