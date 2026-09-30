////////////////////////////////////////////////////////////
// This is the simulation testcase for the Single Port RAM
////////////////////////////////////////////////////////////

module tc_single_port_ram();

    parameter ADDR_WIDTH = 10;
    parameter DATA_WIDTH = 8;

    logic clk;
    logic we;
    logic [ADDR_WIDTH-1:0] addr;
    logic [DATA_WIDTH-1:0] din;
    logic [DATA_WIDTH-1:0] dout;

    single_port_ram #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH)
    ) inst (
        .clk(clk),
        .we(we),
        .addr(addr),
        .din(din),
        .dout(dout)
    );

    always begin
        #5 clk = 1;
        #5 clk = 0;
    end

    initial begin
        #10;
        din = 8'hAB;
        addr = 10'd0;
        we = 1;
        #20;
        din = 8'hBC;
        addr = 10'd512;
        #20;
        din = 8'hCD;
        addr = 10'd1023;
        we = 0;
        #20;
        addr = 10'd0;
        #20;
        addr = 10'd512;
        #20;
        addr = 10'd1023;
        #20;
        $finish;
    end

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars;
    end

endmodule