#!/usr/bin/env python

import random
import xmostest
from  usb_packet import *
from usb_clock import Clock
from helpers import do_rx_test, packet_processing_time, get_dut_address
from helpers import choose_small_frame_size, check_received_packet, runall_rx

def do_test(arch, clk, phy, seed):
    rand = random.Random()
    rand.seed(seed)

    ep = 3

    packets = []

    data_val = 0;
    pkt_length = 20
    data_pid = 0x3 #DATA0 

    for pkt_length in range(10, 20):

        # < 17 fails
        AppendOutToken(packets, ep, inter_pkt_gap=17)
        packets.append(TxDataPacket(rand, data_start_val=data_val, length=pkt_length, pid=data_pid)) #DATA0

        AppendInToken(packets, ep, inter_pkt_gap=37)
        packets.append(RxDataPacket(rand, data_start_val=data_val, length=pkt_length, pid=data_pid))

        data_val = data_val + pkt_length
        #data_pid = data_pid ^ 8

    do_rx_test(arch, clk, phy, packets, __file__, seed,
               level='smoke', extra_tasks=[])

def runtest():
    random.seed(1)
    runall_rx(do_test)
