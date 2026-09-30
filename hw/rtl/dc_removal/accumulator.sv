////////////////////////////////////////////////////////////
// This is the rtl for an accumulator
////////////////////////////////////////////////////////////

module accumulator #(
    parameter DATA_WIDTH = 8
)(
    input logic clk,
    input logic rst,
    input logic en,
    input logic [DATA_WIDTH-1:0] din,
    output logic [DATA_WIDTH-1:0] dout
);

    logic [18:0] total;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) 
            total <= 18'b0;
        else begin
            if (en) 
                dout <= total;
            else begin
                total <= total + din;
            end
        end
        
    end

endmodule
