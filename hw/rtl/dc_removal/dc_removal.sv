////////////////////////////////////////////////////////////
// This is the top level rtl for the DC Offset Removal IP
////////////////////////////////////////////////////////////

module dc_removal #(
    parameter ADDR_WIDTH = 10,
    parameter DATA_WIDTH = 8
)(
    input logic clk;
    input logic rst;
    input [DATA_WIDTH-1:0] I;
    input [DATA_WIDTH-1:0] Q;
);

    logic [ADDR_WIDTH:0]addr;

    // Accumulator for the I samples
    accumulator #(
        .DATA_WIDTH(DATA_WIDTH)
    ) I (
        .clk(clk),
        .rst(rst),
        .en(),
        .din(I),
        .dout()
    );

    // Accumulator for the Q samples
    accumulator #(
        .DATA_WIDTH(DATA_WIDTH)
    ) Q (
        .clk(clk),
        .rst(rst),
        .en(),
        .din(Q),
        .dout()
    );

    // Signle port RAM for the I samples
    single_port_ram #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH)
    ) I (
        .clk(clk),
        .we(),
        .addr(addr),
        .din(I),
        .dout()
    )

    // Signle port RAM for the Q samples
    single_port_ram #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH)
    ) Q (
        .clk(clk),
        .we(),
        .addr(addr),
        .din(Q),
        .dout()
    )

    // IQ Sample Counter
    iq_counter #(
        .WIDTH(ADDR_WIDTH)
    ) inst(
        .en(),
        .rst(),
        .clk(clk),
        .iq_count(addr)
    );


endmodule