////////////////////////////////////////////////////////////
// This is the simulation testcase for the IQ sample counter
////////////////////////////////////////////////////////////

module tc_iq_counter();

    parameter WIDTH = 10;

    logic en;
    logic rst;
    logic clk;
    logic [WIDTH-1:0] iq_count;

    iq_counter #(
        .WIDTH(WIDTH)
    ) inst(
        .en         (en),
        .rst        (rst),
        .clk        (clk),
        .iq_count   (iq_count)
    );

    always begin
        #5 clk = 1;
        #5 clk = 0;
    end

    initial begin
        en = 0;
        rst = 1;
        #10;
        rst = 0;
        en = 1;

        #500;
        $finish;
    end

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars;
    end    

endmodule