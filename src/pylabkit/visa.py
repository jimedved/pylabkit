import pyvisa


class VisaSession:
    """Small wrapper around PyVISA ResourceManager.

    By default, this uses the installed VISA backend, for example NI-VISA.
    """

    def __init__(self, backend: str | None = None) -> None:
        if backend is None:
            self.rm = pyvisa.ResourceManager()
        else:
            self.rm = pyvisa.ResourceManager(backend)

    def list_resources(self) -> tuple[str, ...]:
        return self.rm.list_resources()

    def open_resource(self, resource_name: str, **kwargs):
        return self.rm.open_resource(resource_name, **kwargs)

    def close(self) -> None:
        self.rm.close()
