from pylabkit.instruments.base import VisaInstrument


def main() -> None:
    resource_name = "GPIB0::4::INSTR"

    with VisaInstrument(resource_name) as instrument:
        print("Connected instrument:")
        print(instrument.idn())


if __name__ == "__main__":
    main()