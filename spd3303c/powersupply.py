import time
import os

SPD3303C_CH_1 = "CH1"
SPD3303C_CH_1 = "CH2"

SPD3303C_CMD_IDN = "*IDN?"
SPD3303C_CMD_SAV = "*SAV"
SPD3303C_CMD_RCL = "*RCL"
SPD3303C_CMD_SET_CHANNEL = "INSTrument"
SPD3303C_CMD_GET_CHANNEL = "INSTrument?"
SPD3303C_CMD_MEASURE_CURRENT = "MEASure:CURRent?"
SPD3303C_CMD_MEASURE_VOLTAGE = "MEASure:VOLTage?"
SPD3303C_CMD_SET_CURRENT = ":CURRent"
SPD3303C_CMD_GET_CURRENT = ":CURRent?"
SPD3303C_CMD_SET_VOLTAGE = ":VOLTage"
SPD3303C_CMD_GET_VOLTAGE = ":VOLTage?"
SPD3303C_CMD_SET_OUTPUT = "OUTPut"
SPD3303C_CMD_SET_OUTPUT_MODE = "OUTPut:TRACK"
SPD3303C_CMD_GET_SYSTEM_ERROR = "SYSTem:ERRor?"
SPD3303C_CMD_GET_SYSTEM_VERSION = "SYSTem:VERSion?"
SPD3303C_CMD_GET_SYSTEM_STATUS = "SYSTem:STATus?"
SPD3303C_CMD_LOCK = "*LOCK"
SPD3303C_CMD_UNLOCK = "*UNLOCK"


class SPD3303C:
    def __init__(self, port: str):
        self._port = port
        self._file = None

    def is_open(self):
        return self._file != None

    def open(self):
        self._file = open(self._port, "w+")

    def close(self):
        self._file.close()

    def _send_command(self, command: str, has_response = False):
        self._file.write(command)
        self._file.flush()
        # probably not the best way but the protocol here is so bad
        # that i can't bother to find a better way.
        response = None
        if has_response:
            time.sleep(0.1)
            response = os.read(self._file.fileno(), 50).strip()
            response = response.decode()

        return response

    def get_idn(self):
        return self._send_command(SPD3303C_CMD_IDN, has_response=True)

    def save_state(self, name: str):
        return self._send_command(f"{SPD3303C_CMD_SAV} {name}")

    def load_state(self, name: str):
        return self._send_command(f"{SPD3303C_CMD_RCL} {name}")

    def set_channel(self, channel: str):
        return self._send_command(f"{SPD3303C_CMD_SET_CHANNEL} {channel}")

    def get_channel(self):
        return self._send_command(f"{SPD3303C_CMD_GET_CHANNEL}", has_response=True)

    def measure_current(self, channel: str):
        return float(self._send_command(f"{SPD3303C_CMD_MEASURE_CURRENT} {channel}", has_response=True))

    def measure_voltage(self, channel: str):
        return float(self._send_command(f"{SPD3303C_CMD_MEASURE_VOLTAGE} {channel}", has_response=True))

    def get_current(self, channel: str):
        return float(self._send_command(f"{channel}{SPD3303C_CMD_GET_CURRENT}", has_response=True))

    def set_current(self, channel: str, current: float):
        return self._send_command(f"{channel}{SPD3303C_CMD_SET_CURRENT} {current}")

    def get_voltage(self, channel: str):
        return float(self._send_command(f"{channel}{SPD3303C_CMD_GET_VOLTAGE}", has_response=True))

    def set_voltage(self, channel: str, voltage: float):
        return self._send_command(f"{channel}{SPD3303C_CMD_SET_VOLTAGE} {voltage}")

    def set_output(self, channel: str, enabled: bool):
        state = "ON" if enabled else "OFF"
        return self._send_command(
            f"{SPD3303C_CMD_SET_OUTPUT} {channel},{state}"
        )

    def set_output_mode(self, mode: str):
        return self._send_command(f"{SPD3303C_CMD_SET_OUTPUT_MODE} {mode}")

    def get_system_error(self):
        return self._send_command(f"{SPD3303C_CMD_GET_SYSTEM_ERROR}", has_response=True)

    def get_version(self):
        return self._send_command(f"{SPD3303C_CMD_GET_SYSTEM_VERSION}", has_response=True)

    def get_status(self):
        return self._send_command(f"{SPD3303C_CMD_GET_SYSTEM_STATUS}", has_response=True)

    def lock(self):
        return self._send_command(f"{SPD3303C_CMD_LOCK}")

    def unlock(self):
        return self._send_command(f"{SPD3303C_CMD_UNLOCK}")
