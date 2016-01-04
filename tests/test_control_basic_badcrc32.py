#!/usr/bin/env python

import random
import xmostest
from usb_packet import *
from usb_clock import Clock
from helpers import do_rx_test, packet_processing_time, get_dut_address
from helpers import choose_small_frame_size, check_received_packet, runall_rx


# Single, setup transaction to EP 0

def do_test(arch, tx_clk, tx_phy, seed):
    rand = random.Random()
    rand.seed(seed)

    dev_address = get_dut_address()
    ep = 0

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    AppendSetupToken(packets, ep)

    # DATA0 data packet with bad CRC
    packets.append(TxDataPacket(rand, length=8, pid=3, bad_crc=True))
 
    # Dont expect an ACK due to bad CRC
    #packets.append(RxHandshakePacket())

    AppendSetupToken(packets, ep, inter_pkt_gap=400)
    packets.append(TxDataPacket(rand, length=8, pid=3, bad_crc=False ))
    packets.append(RxHandshakePacket(timeout=11))

    # Note, quite big gap to allow checking.

    AppendOutToken(packets, ep, inter_pkt_gap=2000)
    
    packets.append(TxDataPacket(rand, length=10, pid=0xb))
    
    packets.append(RxHandshakePacket())

    #IN
    AppendInToken(packets, ep, inter_pkt_gap=500)

    #Expect 0-length
    packets.append(RxDataPacket(rand, length=0, pid=0x4b))

    # Send ACK
    packets.append(TxHandshakePacket())

    do_rx_test(arch, tx_clk, tx_phy, packets, __file__, seed,
               level='smoke', extra_tasks=[])

def runtest():
    random.seed(1)
    runall_rx(do_test)
