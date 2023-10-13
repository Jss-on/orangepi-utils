import os
import logging
import subprocess
from typing import List, Dict

# Initialize logging
logging.basicConfig(level=logging.INFO)


class GPIO:
    def __init__(self) -> None:
        self.base_path: str = "/sys/class/gpio"
        self.led_base_path: str = "/sys/class/leds"
        logging.info("OPIGPIO initialized.")

    def _get_led_path(self, led_name: str) -> str:
        full_led_name = (
            f"orangepi:{led_name}:pwr"
            if led_name == "green"
            else f"orangepi:{led_name}:status"
        )
        return os.path.join(self.led_base_path, full_led_name, "brightness")

    def _is_led(self, pin_label: str) -> bool:
        return pin_label in ["green", "red"]

    def _change_permissions(self, path: str) -> None:
        try:
            subprocess.run(["sudo", "chmod", "666", path])
            logging.info(f"Changed permissions for {path}.")
        except Exception as e:
            logging.error(f"Failed to change permissions for {path}: {e}")

    def _write_to_file(self, path: str, value: str) -> None:
        try:
            with open(path, "w") as f:
                f.write(str(value))
            logging.info(f"Successfully wrote {value} to {path}.")
        except PermissionError:
            logging.warning(
                f"Permission error while trying to write to {path}. Changing permissions..."
            )
            self._change_permissions(path)
            self._write_to_file(path, value)
        except IOError as e:
            logging.error(f"Failed to write to {path}: {e}")

    def _read_from_file(self, path: str) -> str:
        try:
            with open(path, "r") as f:
                val = f.read().strip()
            logging.info(f"Successfully read value {val} from {path}.")
            return val
        except PermissionError:
            logging.warning(
                f"Permission error while trying to read from {path}. Changing permissions..."
            )
            self._change_permissions(path)
            return self._read_from_file(path)
        except IOError as e:
            logging.error(f"Failed to read from {path}: {e}")
            return ""

    def setup(self) -> None:
        logging.info("Setup complete.")

    def togglePin(self, pin_label: str) -> None:
        value = self.digitalRead(pin_label)
        self.digitalWrite(pin_label, 1 - value)

    def pinModeAll(self, pins: List[int], mode: str) -> None:
        for pin in pins:
            self.pinMode(pin, mode)

    def digitalWriteAll(self, pins: List[int], value: int) -> None:
        for pin in pins:
            self.digitalWrite(pin, value)

    def digitalReadAll(self, pins: List[int]) -> List[int]:
        return [self.digitalRead(pin) for pin in pins]

    def isExported(self, pin: int) -> bool:
        gpio_path = os.path.join(self.base_path, f"gpio{pin}")
        return os.path.exists(gpio_path)

    def setPullUp(self, pin: int, state: str) -> None:
        gpio_path = os.path.join(self.base_path, f"gpio{pin}")
        pullup_path = os.path.join(gpio_path, "pullup")
        self._write_to_file(pullup_path, state)

    def getPinInfo(self, pin: int) -> Dict[str, str]:
        gpio_path = os.path.join(self.base_path, f"gpio{pin}")
        if not os.path.exists(gpio_path):
            logging.error(f"Pin {pin} is not exported.")
            return {}

        direction_path = os.path.join(gpio_path, "direction")
        value_path = os.path.join(gpio_path, "value")

        direction = self._read_from_file(direction_path)
        value = self._read_from_file(value_path)

        return {"direction": direction, "value": value}

    @staticmethod
    def convertPinLabelToNumber(pin_label: str) -> int:
        if not pin_label or len(pin_label) < 3 or pin_label[0] != "P":
            return -1  # Invalid pin label

        letter = pin_label[1].upper()
        number_str = pin_label[2:]

        try:
            number = int(number_str)
        except ValueError:
            return -1  # Invalid pin number part

        letter_position = ord(letter) - ord("A") + 1
        pin_number = (letter_position - 1) * 32 + number
        return pin_number

    # Modified pinMode method to handle both GPIO pins and built-in LEDs
    def pinMode(self, pin_label: str, mode: str) -> None:
        if self._is_led(pin_label):
            # LEDs don't have a 'mode' in the traditional sense, but you could add
            # custom logic here if needed.
            led_path = self._get_led_path(pin_label)
            if not os.path.exists(led_path):
                logging.error(f"LED {pin_label} does not exist.")
                return
            logging.info(f"Checked existence of LED {pin_label}.")
        else:
            pin = self.convertPinLabelToNumber(pin_label)
            if pin == -1:
                logging.error(f"Invalid pin label {pin_label}.")
                return
            export_path = os.path.join(self.base_path, "export")
            self._write_to_file(export_path, str(pin))

            gpio_path = os.path.join(self.base_path, f"gpio{pin}")
            direction_path = os.path.join(gpio_path, "direction")
            self._write_to_file(direction_path, mode)

            logging.info(f"Set mode {mode} for pin {pin_label} ({pin}).")

    def digitalWrite(self, pin_label: str, value: int) -> None:
        if self._is_led(pin_label):
            led_path = self._get_led_path(pin_label)
            self._write_to_file(led_path, str(value))
            logging.info(f"Wrote value {value} to LED {pin_label}.")
        else:
            pin = self.convertPinLabelToNumber(pin_label)
            if pin == -1:
                logging.error(f"Invalid pin label {pin_label}.")
                return
            gpio_path = os.path.join(self.base_path, f"gpio{pin}")
            value_path = os.path.join(gpio_path, "value")
            self._write_to_file(value_path, str(value))
            logging.info(f"Wrote value {value} to pin {pin_label} ({pin}).")

    def digitalRead(self, pin_label: str) -> int:
        if self._is_led(pin_label):
            led_path = self._get_led_path(pin_label)
            value = int(self._read_from_file(led_path))
            logging.info(f"Read value {value} from LED {pin_label}.")
            return value
        else:
            pin = self.convertPinLabelToNumber(pin_label)
            if pin == -1:
                logging.error(f"Invalid pin label {pin_label}.")
                return -1
            gpio_path = os.path.join(self.base_path, f"gpio{pin}")
            value_path = os.path.join(gpio_path, "value")
            value = int(self._read_from_file(value_path))
            logging.info(f"Read value {value} from pin {pin_label} ({pin}).")
            return value

    def unexport(self, pin_label: str) -> None:
        pin = self.convertPinLabelToNumber(pin_label)
        if pin == -1:
            logging.error(f"Invalid pin label {pin_label}.")
            return
        unexport_path = os.path.join(self.base_path, "unexport")
        self._write_to_file(unexport_path, str(pin))

        logging.info(f"Unexported pin {pin_label} ({pin}).")
