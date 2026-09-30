////////////////////////////////////////////////////////////
// This is the simulation testcase for the data cleaner
////////////////////////////////////////////////////////////

module tc_data_cleaner();

    parameter DATA_WIDTH = 8;

    logic clk;
    logic rst;
    logic [DATA_WIDTH-1:0] I_dc;
    logic [DATA_WIDTH-1:0] Q_dc;
    logic [DATA_WIDTH-1:0] stored_I;
    logic [DATA_WIDTH-1:0] stored_Q;
    logic [DATA_WIDTH-1:0] clean_I;
    logic [DATA_WIDTH-1:0] clean_Q;

    data_cleaner #(
        .DATA_WIDTH(DATA_WIDTH)
    ) inst (
        .clk(clk),
        .rst(rst),
        .I_dc(I_dc),
        .Q_dc(Q_dc),
        .stored_I(stored_I),
        .stored_Q(stored_Q),
        .clean_I(clean_I),
        .clean_Q(clean_Q)
    );

    always begin
        #5 clk = 1;
        #5 clk = 0;
    end

    initial begin
        rst = 1'b1;
        I_dc = 8'd2;
        Q_dc = 8'd3;
        #10;
        rst = 1'b0;
        stored_I = 8;
        stored_Q = 6;
        #10;
        stored_I = 10;
        stored_Q = 5;
        #10;
        stored_I = 3;
        stored_Q = 1;
        #30;
        $finish;
    end


    initial begin
        $dumpfile("dump.vcd");
        $dumpvars;
    end

endmodule