import time

from pylabkit.instruments.base import VisaInstrument


RESOURCE_NAME = "GPIB0::4::INSTR"


def safe_write(instrument: VisaInstrument, command: str, delay_s: float = 0.3) -> None:
    print(f"> {command}")
    instrument.write(command)
    time.sleep(delay_s)


def main() -> None:
    with VisaInstrument(RESOURCE_NAME, timeout_ms=20_000) as lcr:
        print("Connected to QT7600")

        print("Configuring measurement...")

        safe_write(lcr, "CONF:FREQ 1000.00")
        safe_write(lcr, "CONF:PPAR RS")
        safe_write(lcr, "CONF:SPAR Q")
        safe_write(lcr, "CONF:MAC ENH")
        safe_write(lcr, "CONF:NOM 0")
        safe_write(lcr, "CONF:DISP M")

        print("Triggering measurement...")
        safe_write(lcr, "MEAS:", delay_s=1.0)

        print("Fetching result...")
        raw = lcr.query("FETC?")

        print()
        print("Raw response:")
        print(raw)

        tokens = raw.split()

        print()
        print("Split tokens:")
        for index, token in enumerate(tokens):
            print(f"{index}: {token}")

        if len(tokens) >= 5:
            primary_parameter = tokens[0]
            primary_value = float(tokens[1])
            primary_unit = tokens[2]

            secondary_parameter = tokens[3]
            secondary_value = float(tokens[4])

            print()
            print("Parsed measurement:")
            print(f"Primary parameter:   {primary_parameter}")
            print(f"Primary value:       {primary_value}")
            print(f"Primary unit:        {primary_unit}")
            print(f"Secondary parameter: {secondary_parameter}")
            print(f"Secondary value:     {secondary_value}")
        else:
            print("Could not parse response.")


if __name__ == "__main__":
    main()