from __future__ import annotations

import time

from pylabkit.instruments.basic import VisaInstrument
from pylabkit.instruments.lcr import LCRMeter, LCRReading


class QuadTech7600(VisaInstrument, LCRMeter):
    """Driver for the QuadTech 7600 Precision LCR Meter."""

    def __init__(
        self,
        resource_name: str,
        timeout_ms: int = 10_000,
        read_termination: str = "\n",
        write_termination: str = "\n",
        measurement_delay_s: float = 0.1,
    ) -> None:
        super().__init__(
            resource_name=resource_name,
            timeout_ms=timeout_ms,
            read_termination=read_termination,
            write_termination=write_termination,
        )

        self.measurement_delay_s = measurement_delay_s

        self._frequency_hz: float | None = None
        self._primary_parameter: str | None = None
        self._secondary_parameter: str | None = None

    def recall_default_setup(self) -> None:
        """Recall the default instrument setup."""
        self.write("CONF:REC DEFAULT")

    def set_frequency(self, frequency_hz: float) -> None:
        """Set the measurement frequency in hertz."""
        self.write(f"CONF:FREQ {frequency_hz}")
        self._frequency_hz = frequency_hz

    def set_ac_voltage(self, voltage_v: float) -> None:
        """Set the AC test voltage.

        This command is intentionally not implemented yet because the
        exact remote command must be verified in the instrument manual.
        """
        raise NotImplementedError(
            "AC voltage setting is not implemented yet for the QuadTech 7600."
        )

    def set_primary_parameter(self, parameter: str) -> None:
        """Set the primary measurement parameter.

        Examples
        --------
        CS, CP, LS, LP, RS, RP
        """
        parameter = parameter.upper()
        self.write(f"CONF:PPAR {parameter}")
        self._primary_parameter = parameter

    def set_secondary_parameter(self, parameter: str) -> None:
        """Set the secondary measurement parameter.

        Examples
        --------
        DF, Q
        """
        parameter = parameter.upper()
        self.write(f"CONF:SPAR {parameter}")
        self._secondary_parameter = parameter

    def set_measurement_accuracy(self, mode: str = "ENH") -> None:
        """Set the measurement accuracy mode.

        The manual example uses ENH.
        """
        self.write(f"CONF:MAC {mode.upper()}")

    def set_nominal_value(self, value: float = 0) -> None:
        """Set the nominal value used by the instrument."""
        self.write(f"CONF:NOM {value}")

    def set_display_mode(self, mode: str = "M") -> None:
        """Set the display mode.

        The manual example uses M.
        """
        self.write(f"CONF:DISP {mode.upper()}")

    def setup_default_lcr_measurement(
        self,
        frequency_hz: float = 1000.0,
        primary_parameter: str = "CS",
        secondary_parameter: str = "DF",
        accuracy_mode: str = "ENH",
    ) -> None:
        """Configure a basic LCR measurement using the manual example sequence."""
        self.recall_default_setup()
        self.set_frequency(frequency_hz)
        self.set_primary_parameter(primary_parameter)
        self.set_secondary_parameter(secondary_parameter)
        self.set_measurement_accuracy(accuracy_mode)
        self.set_nominal_value(0)
        self.set_display_mode("M")

    def trigger_measurement(self) -> None:
        """Start one measurement."""
        self.write("MEAS:")

    def fetch(self) -> LCRReading:
        """Fetch the latest measurement result."""
        raw = self.query("FETC?")
        return self._parse_reading(raw)

    def measure(self) -> LCRReading:
        """Trigger one measurement and fetch the result."""
        self.trigger_measurement()
        time.sleep(self.measurement_delay_s)
        return self.fetch()

    def _parse_reading(self, raw: str) -> LCRReading:
        """Parse the raw response returned by the instrument.

        The QuadTech 7600 can return several comma-separated fields.
        For now, PyLabKit extracts the first two numeric fields and
        always keeps the raw response.
        """
        fields = [field.strip() for field in raw.split(",")]

        primary = None
        secondary = None

        if len(fields) >= 1:
            primary = self._try_float(fields[0])

        if len(fields) >= 2:
            secondary = self._try_float(fields[1])

        return LCRReading(
            primary=primary,
            secondary=secondary,
            frequency_hz=self._frequency_hz,
            primary_parameter=self._primary_parameter,
            secondary_parameter=self._secondary_parameter,
            raw=raw,
        )

    @staticmethod
    def _try_float(value: str) -> float | None:
        """Try to convert a field to float."""
        try:
            return float(value)
        except ValueError:
            return None