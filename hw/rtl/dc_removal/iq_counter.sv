///////////////////////////////////////////
// This is the rtl for the IQ sample counter
///////////////////////////////////////////

timeunit 1ns;
timeprecision 1ns;

module iq_counter #(
	parameter int WIDTH = 10
)(
    input logic rst,
    input logic clk,
    output logic [WIDTH-1:0] iq_count
);

    always_ff @(posedge clk, posedge rst) begin
        if (rst)
            iq_count <= 0;
        else begin
            iq_count <= iq_count + 1'b1;
        end
    end

endmodule
