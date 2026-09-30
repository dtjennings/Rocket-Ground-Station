////////////////////////////////////////////////////////////
// This is the rtl used to clean each IQ sample using the mean subtract method
////////////////////////////////////////////////////////////

timeunit 1ns;
timeprecision 1ns;

module data_cleaner #(
    parameter int DATA_WIDTH = 8
)(
    input logic clk,
    input logic rst,
    input logic [DATA_WIDTH-1:0] I_dc,
    input logic [DATA_WIDTH-1:0] Q_dc,
    input logic [DATA_WIDTH-1:0] stored_I,
    input logic [DATA_WIDTH-1:0] stored_Q,
    output logic [DATA_WIDTH-1:0] clean_I,
    output logic [DATA_WIDTH-1:0] clean_Q
);

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            clean_I <= 0;
            clean_Q <= 0;
        end
        else begin
            clean_I <= stored_I - I_dc;
            clean_Q <= stored_Q - Q_dc;
        end
    end

endmodule