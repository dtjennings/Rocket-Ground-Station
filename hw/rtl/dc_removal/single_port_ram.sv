////////////////////////////////////////////////////////////
// This is the rtl for single port RAM
////////////////////////////////////////////////////////////

module single_port_ram #(
    ADDR_WIDTH = 10,
    DATA_WIDTH = 8
)(
    input logic clk,
    input logic we,
    input logic [ADDR_WIDTH-1:0] addr,
    input logic [DATA_WIDTH-1:0] din,
    output logic [DATA_WIDTH-1:0] dout
);

    // Declare memory array
    logic [DATA_WIDTH-1:0] ram [2**ADDR_WIDTH];

    // Read and Write
    always_ff @(posedge clk) begin
        if (we) begin
            ram[addr] <= din;
        end
        else
            dout <= ram[addr];
    end

endmodule