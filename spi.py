# -*- coding: utf-8 -*-

import veriloggen as vg


def make_spi_receiver():
    m = vg.Module("spi-receiver")

    interval = m.Parameter("INTERVAL", 24_000_000 // 192_000)

    sclk = m.Input("SCLK")
    rst = m.Input("RST")
    cs = m.Input("CS")
    input_reg = m.Input("INPUT", 8)
    output_reg = m.OutputReg("OUTPUT", 8, initval=0)

    count = m.Reg("count", 32, initval=0)
    comm_clk = m.Reg("COMM_CLK", initval=0)

    seq = vg.Seq(m, "seq", sclk, rst)
    seq.add(vg.Systask("display", "count:%d"), count)
    seq.add(count(count + 1), cond=(count < interval - 1))
    seq.add(count(0), cond=(count == interval - 1))
    seq.add(comm_clk(~comm_clk), cond=(count == interval - 1))
    seq.make_always()

    return m


def mkTest():
    m = vg.Module("test")
    # target instance
    spi_recv = make_spi_receiver()

    # copy paras and ports
    params = m.copy_params(spi_recv)
    ports = m.copy_sim_ports(spi_recv)
    clk = ports["SCLK"]
    rst = ports["RST"]

    uut = m.Instance(spi_recv, "uut", params=m.connect_params(spi_recv), ports=m.connect_ports(spi_recv))

    # simulation.setup_waveform(m, uut)
    vg.simulation.setup_waveform(m, uut, m.get_vars())
    vg.simulation.setup_clock(m, clk, hperiod=5)
    init = vg.simulation.setup_reset(m, rst, m.make_reset(), period=100)
    init.add(
        vg.Delay(1000),
        vg.Systask("finish"),
    )
    return m


if __name__ == "__main__":
    test = mkTest()
    verilog = test.to_verilog("tmp.v")
    print(verilog)
    sim = vg.simulation.Simulator(test)
    rslt = sim.run()
    print(rslt)
    # sim.view_waveform()
