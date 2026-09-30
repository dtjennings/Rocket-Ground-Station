////////////////////////////////////////////////////////////
// This is the simulation testcase for the DC removal IP
////////////////////////////////////////////////////////////

module tc_dc_removal ();

    parameter ADDR_WIDTH = 10;
    parameter DATA_WIDTH = 8;

    localparam real PI = 3.141592654;
    localparam real CYCLES = 4;

    real AMPLITUDE = 50;
    real DC_I = 20;
    real DC_Q = -10;
    real angle;

    logic clk = 1'b0;
    logic rst;
    logic signed [DATA_WIDTH-1:0] I;
    logic signed [DATA_WIDTH-1:0] Q;
    logic signed [DATA_WIDTH-1:0] I_clean;
    logic signed [DATA_WIDTH-1:0] Q_clean;

    dc_removal #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH)
    ) inst (
        .clk(clk),
        .rst(rst),
        .I(I),
        .Q(Q),
        .I_clean(I_clean),
        .Q_clean(Q_clean)
    );

    always #5 clk = ~clk;

    initial begin
        rst = 1;
        #10;
        rst = 0;
        #10;

        for (int i = 0; i < 2**ADDR_WIDTH; i++) begin
            angle = 2 * PI * (CYCLES/2**ADDR_WIDTH) * i;
            I = $rtoi(AMPLITUDE * $cos(angle) + DC_I);
            Q = $rtoi(AMPLITUDE * $sin(angle) + DC_Q);

            #10;
        end

        #10000;
        $finish;

    end

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars;
    end

endmodule