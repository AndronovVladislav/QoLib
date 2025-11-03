import time

from psutil import Process, net_connections
from psutil._common import NoSuchProcess
from rich.live import Live
from typer import Option

from src.core import app, console
from src.modules.ports import show_ports


@app.command()
def ports(
    port: int = Option(-1, '--port', '-p', help='Port to kill'),
    kill: bool = Option(False, '--kill', '-k', help='Kill the process using the port specified in -p.'),
) -> None:
    if kill:
        _kill_process(port)
    else:
        _show_ports()


def _kill_process(port: int) -> None:
    if port == -1:
        raise ValueError('Port must be specified in -p.')

    process = _get_process_by_port(port)

    if process:
        process.kill()
        message = f'[green]{process.name()} killed!'
    else:
        message = f'[red]Process using {port} port does not exist!'

    console.print(message)


def _get_process_by_port(port: int) -> Process | None:
    for conn in net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port and conn.pid:
            try:
                proc = Process(conn.pid)
                return proc
            except NoSuchProcess:
                return None
    return None


def _show_ports() -> None:
    with Live(show_ports(), refresh_per_second=5) as live:
        for _ in range(25):
            time.sleep(.2)
            live.update(show_ports())
