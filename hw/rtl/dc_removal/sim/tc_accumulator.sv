////////////////////////////////////////////////////////////
// This is the simulation testcase for the Accumulator
////////////////////////////////////////////////////////////

module tc_accumulator();

    parameter DATA_WIDTH = 8;

    logic clk;
    logic rst;
    logic en;
    logic [DATA_WIDTH-1:0] din;
    logic [DATA_WIDTH-1:0] dout;

    accumulator #(
        .DATA_WIDTH(DATA_WIDTH)
    ) I (
        .clk(clk),
        .rst(rst),
        .en(en),
        .din(din),
        .dout(dout)
    );

    always begin
        #5 clk = 1;
        #5 clk = 0;
    end

    initial begin
        rst = 1'b1;
        din = 1'b0;
        #10;
        rst = 1'b0;
        #10;
        din = 1;
        #10;
        din = 2;
        #10;
        din = 3;
        #10;
        en = 1'b1;
        #10;
        rst = 1'b1;
        din = 8'b0;
        #10;
        rst = 1'b0;
        #10;

        $finish;
    end

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars;
    end

endmodule