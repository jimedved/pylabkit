from pylabkit.instruments.basic import VisaInstrument


def main() -> None:
    resource_name = "GPIB0::17::INSTR"

    with VisaInstrument(resource_name) as instrument:
        print("Connected instrument:")
        print(instrument.idn())


if __name__ == "__main__":
    main()