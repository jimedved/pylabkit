from typing import Any #for create objects of "Any" type
from pylabkit.visa import VisaSession # import the class created in visa.py, to open VISA using NI-VISA
from __future__ import annotations

#Create a basic class for all instruments

class VisaInstrument:

    #This is the constructor, the funcion that is call every time we create an object of this class
    # example: instrument=VisaInstruments("GPIB0::17::INSTR")
    def __init__(
        self,
        resource_name: str,         #the str is the address, GPIB0::17:INSTR in the example
        timeout_ms: int = 10_000,
        read_termination: str = "\n",
        write_termination: str = "\n",
    ) -> None:
        self.resource_name = resource_name
        self.timeout_ms = timeout_ms
        self.read_termination = read_termination
        self.write_termination = write_termination

        self.visa = VisaSession()       #it creates a VISA session, using pyVISA
        self.resource: Any | None = None    #there is no connection when is created

    @property

    #only to ask is the instrument is connected
    def is_connected(self) -> bool:
        return self.resource is not None

    #this function first check if the instrument is connected
    # then, using the self.resource_name, opens the connection to the instrument using self.visa.open_resource 
    def connect(self) -> None:
        """Open the VISA resource."""
        if self.resource is not None:
            return

        self.resource = self.visa.open_resource(self.resource_name)
        self.resource.timeout = self.timeout_ms
        self.resource.read_termination = self.read_termination
        self.resource.write_termination = self.write_termination

    # this close the connection
    def close(self) -> None:
        """Close the VISA resource."""
        if self.resource is not None:
            self.resource.close()
            self.resource = None

    # this is a protection, if you create an object but do not connected
    def _check_connected(self) -> None:
        if self.resource is None:
            raise RuntimeError(
                f"Instrument {self.resource_name!r} is not connected. "
                "Call connect() first."
            )

    # send a command to an instrument, first check if it is connected
    def write(self, command: str) -> None:
        """Write a command to the instrument."""
        self._check_connected()
        self.resource.write(command)

    #reads an answer from the instrument
    def read(self) -> str:
        """Read a response from the instrument."""
        self._check_connected()
        return self.resource.read().strip() #strip deletes spaces or '\n'

    # this is a combination of write and read
    def query(self, command: str) -> str:
        """Write a command and read the response."""
        self._check_connected()
        return self.resource.query(command).strip()

    def idn(self) -> str:
        """Return the instrument identification string."""
        return self.query("*IDN?")

    def reset(self) -> None:
        """Reset the instrument."""
        self.write("*RST")

    def clear_status(self) -> None:
        """Clear the instrument status register."""
        self.write("*CLS")

    # the next methods, allow us to use the clase with 'with'
    #the main advantage is that 'with' closes the insturment even if there is an error
    def __enter__(self) -> "VisaInstrument":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()