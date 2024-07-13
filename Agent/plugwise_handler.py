import plugwise
import time

MAC_CIRCLE_PLUS = "000D6F0005A9147D"
PORT = "/dev/ttyUSB0"  # or "com1" at Windows

MACHINE_PLUGS = {
    1: MAC_CIRCLE_PLUS
}

def scan_finished():
    print("== Initialization has finished ==")
    time.sleep(5)
    plugwise1.node(MAC_CIRCLE_PLUS).set_relay_state(True)
    time.sleep(5)
    plugwise1.node(MAC_CIRCLE_PLUS).set_relay_state(False)


def set_relay(machine_id, state, pw):
    mac = MACHINE_PLUGS.get(machine_id)
    if mac is None:
        print(f"Machine {machine_id} is not available")
        return

    pw.node(mac).set_relay_state(state)


if __name__ == "__main__":
    plugwise1 = plugwise.stick(PORT, scan_finished, False)
    time.sleep(300)
    print("stop auto update")
    plugwise1.auto_update(0)

    time.sleep(5)

    print("Exiting ...")
    plugwise1.disconnect()