from __future__ import annotations

from abc import ABC, abstractmethod #ABC = abstract base class
from dataclasses import dataclass


@dataclass #this is a class which objective is to STORE DATA
 #this writes the __init__, do not need to write the constructor
 #also can be used to print results in a better way
 # This class represents a result of a measurement, do not control any instrument, only save data
class LCRReading:
    """Generic measurement result returned by an LCR meter.

    Parameters
    ----------
    primary:
        Value of the primary measured parameter.
    secondary:
        Value of the secondary measured parameter.
    frequency_hz:
        Measurement frequency in hertz.
    primary_parameter:
        Name of the primary measured parameter, for example CS, CP, LS, RS.
    secondary_parameter:
        Name of the secondary measured parameter, for example DF, Q, RP.
    raw:
        Raw response returned by the instrument.
    """

    primary: float | None
    secondary: float | None
    frequency_hz: float | None = None
    primary_parameter: str | None = None
    secondary_parameter: str | None = None
    raw: str | None = None


class LCRMeter(ABC): #imports ABC, this is an ABSTRACT BASE CLASS
    # lcr=LCRMeter() is wrong, because is an ABC... we need to create a new class calling LCRMeter
    """Abstract interface for LCR meters.
    This class defines the common operations that any LCR meter driver
    should implement. It does not contain instrument-specific commands.
    """

# the abstractmethod is useful to say that this method should exist, but it must be implemented by the derived class, is not implemented here
# this is useful because then we can write GENERIC CODE, without the specific implementation of the function

    @abstractmethod
    def set_frequency(self, frequency_hz: float) -> None:
        """Set the measurement frequency in hertz."""
        pass

    @abstractmethod
    def set_ac_voltage(self, voltage_v: float) -> None:
        """Set the AC test voltage in volts."""
        pass

    @abstractmethod
    def set_primary_parameter(self, parameter: str) -> None:
        """Set the primary measurement parameter.

        Examples
        --------
        CS, CP, LS, LP, RS, RP, Z
        """
        pass

    @abstractmethod
    def set_secondary_parameter(self, parameter: str) -> None:
        """Set the secondary measurement parameter.

        Examples
        --------
        DF, Q, RP, RS, X
        """
        pass

    @abstractmethod
    def measure(self) -> LCRReading:
        """Perform a measurement and return the result."""
        pass


    def configure_measurement(
        self,
        frequency_hz: float,
        primary_parameter: str,
        secondary_parameter: str,
        voltage_v: float | None = None,
    ) -> None:
        """Configure a generic LCR measurement.

        This method is common to all LCR meters and calls the abstract
        methods implemented by each specific driver.
        """
        self.set_frequency(frequency_hz)
        self.set_primary_parameter(primary_parameter)
        self.set_secondary_parameter(secondary_parameter)

        if voltage_v is not None:
            self.set_ac_voltage(voltage_v)