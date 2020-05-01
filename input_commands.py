import pyb
import uasyncio as asyncio
import aswitch
import as_GPS
import as_rwGPS

def callback(gps, _, timer):
    timer.trigger(10000)  # Outage is declared after 10s

def cb_timeout():
    global ntimeouts
    ntimeouts += 1

def message_cb(gps, segs):
    print('Message received:', segs)

async def gps_test(command):
    global gps, uart  # For shutdown
    print('Initialising')
    # Adapt UART instantiation for other MicroPython hardware
    uart = pyb.UART(4, 9600, read_buf_len=200)
    # read_buf_len is precautionary: code runs reliably without it.
    sreader = asyncio.StreamReader(uart)
    swriter = asyncio.StreamWriter(uart, {})
    timer = aswitch.Delay_ms(cb_timeout)
    sentence_count = 0
    gps = as_rwGPS.GPS(sreader, swriter, local_offset=1, fix_cb=callback, fix_cb_args=(timer,),  msg_cb = message_cb)
    asyncio.sleep(2)

    if command == "standby":
        print('***** Query STANDBY *****')
        await gps.command(as_rwGPS.STANDBY)

    if command == "warm_start":
        print('***** Query WARM_START *****')
        await gps.command(as_rwGPS.WARM_START)

    if command == "cold_start":
        print('***** Query COLD_START *****')
        await gps.command(as_rwGPS.FULL_COLD_START)
    
    await asyncio.sleep(5)

def send_command(command):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gps_test(command))

