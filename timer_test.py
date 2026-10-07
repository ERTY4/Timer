import time
import tkinter as tk
import unittest

from timer import TimerApp


class TestTimerLogic(unittest.TestCase):
    def setUp(self) -> None:
        """Creates a new instance of the app."""
        self.root = tk.Tk()
        self.app = TimerApp(self.root)

    def tearDown(self) -> None:
        """Closes Tkinter after the test is over."""
        self.root.destroy()

    # parse_input() tests
    def test_parse_input_valid(self) -> None:
        """Checks that parse_input correctly changes input"""
        self.assertEqual(self.app.parse_input("10"), 10)

    def test_parse_input_empty(self) -> None:
        """Checks that empty input returns 0"""
        self.assertEqual(self.app.parse_input(""), 0)

    def test_parse_input_letters(self) -> None:
        """Checks that strings dont cause an error"""
        self.assertEqual(self.app.parse_input("abc"), 0)

    def test_parse_input_negative(self) -> None:
        """Checks for negative integers"""
        self.assertEqual(self.app.parse_input("-5"), 0)

    def test_parse_input_out_of_bounds(self) -> None:
        """Check the 12 hours limit"""
        self.assertEqual(self.app.parse_input("800"), 0)

    # update_timer_preview() tests
    def test_preview_with_hour_overflow(self) -> None:
        """Check return if minutes are more or equal 60"""
        self.app.work_check.set("50")
        self.app.rest_check.set("20")

        self.app.update_timer_preview()

        self.assertEqual(self.app.timer_check.get(), "00:50-01:10")

    def test_preview_with_invalid_input(self) -> None:
        """Checks if invalid inputs doesnt cause an error"""
        self.app.work_check.set("invalid")
        self.app.rest_check.set("15")

        self.app.update_timer_preview()

        # Так как 'invalid' станет 0, превью должно показать 00:00-00:15
        self.assertEqual(self.app.timer_check.get(), "00:00-00:15")

    # toggle_timer() tests
    def test_toggle_timer_starts_successfully(self) -> None:
        """Check if all variables work upon initializing"""
        self.app.work_check.set("15")
        self.app.rest_check.set("5")

        self.app.toggle_timer()

        self.assertTrue(self.app.is_running)
        self.assertEqual(self.app.phase, "work")
        self.assertEqual(self.app.work_seconds, 900)  # 15 * 60
        self.assertEqual(self.app.rest_seconds, 300)  # 5 * 60
        self.assertGreater(self.app.end_time, time.perf_counter())

    def test_toggle_timer_blocks_zero_input(self) -> None:
        """Checks that timer doesnt run when one of the times is 0"""
        self.app.work_check.set("0")
        self.app.rest_check.set("10")

        self.app.toggle_timer()

        self.assertFalse(self.app.is_running)

    def test_toggle_timer_stops_running_timer(self) -> None:
        """Checks the starting of the timer"""
        self.app.is_running = True
        self.app.phase = "rest"
        self.app.work_rest_change.set("Rest")

        self.app.toggle_timer()

        self.assertFalse(self.app.is_running)
        self.assertEqual(self.app.time_output.get(), "00:00:00")
        self.assertEqual(self.app.work_rest_change.get(), "Work")
        self.assertEqual(str(self.app.current_timer.cget("foreground")), "#bb0000")


if __name__ == "__main__":
    unittest.main()
