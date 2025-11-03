from psutil import net_connections, CONN_LISTEN, Process, NoSuchProcess
from rich.align import Align
from rich.box import ROUNDED
from rich.table import Table

PORTS_TABLE_COLUMNS = ('PID', 'Port', 'Process Name', 'Address')


def show_ports():
    table = Table(title='Listening Ports', box=ROUNDED)

    for column in PORTS_TABLE_COLUMNS:
        table.add_column(column)

    for conn in sorted(net_connections(), key=lambda x: -x.laddr.port):
        if conn.status != CONN_LISTEN:
            continue

        local_address = f'{conn.laddr.ip if conn.laddr else ''}'
        port = f'{conn.laddr.port if conn.laddr else ''}'
        pid = conn.pid or '-'

        try:
            name = Process(pid).name() if pid != '-' else '-'
        except NoSuchProcess:
            name = '-'

        table.add_row(str(pid), str(port), name, local_address)

    return Align.center(table)
