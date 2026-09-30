////////////////////////////////////////////////////////////
// This is the top level rtl for the DC Offset Removal IP
////////////////////////////////////////////////////////////

timeunit 1ns;
timeprecision 1ns;

`include "accumulator.sv"
`include "data_cleaner.sv"
`include "iq_counter.sv"
`include "single_port_ram.sv"

module dc_removal #(
    parameter ADDR_WIDTH = 10,
    parameter DATA_WIDTH = 8
)(
    input logic clk,
    input logic rst,
    input logic [DATA_WIDTH-1:0] I,
    input logic [DATA_WIDTH-1:0] Q,
    output logic [DATA_WIDTH-1:0] I_clean,
    output logic [DATA_WIDTH-1:0] Q_clean
);

    logic [ADDR_WIDTH-1:0]addr;
    logic we;
    logic done;
    logic en;
    logic [17:0] total_I;
    logic [17:0] total_Q;
    logic [DATA_WIDTH-1:0] stored_I;
    logic [DATA_WIDTH-1:0] stored_Q;

    logic [DATA_WIDTH-1:0] I_dc;
    logic [DATA_WIDTH-1:0] Q_dc;

    // Subtract the DC offsets from the IQ values
    data_cleaner #(
        .DATA_WIDTH(DATA_WIDTH)
    ) inst (
        .clk(clk),
        .rst(rst),
        .I_dc(I_dc),
        .Q_dc(Q_dc),
        .stored_I(stored_I),
        .stored_Q(stored_Q),
        .clean_I(I_clean),
        .clean_Q(Q_clean)
    );

    // Accumulator for the I samples
    accumulator #(
        .DATA_WIDTH(DATA_WIDTH)
    ) I_acc (
        .clk(clk),
        .rst(rst),
        .en(done),
        .din(I),
        .dout(total_I)
    );

    // Accumulator for the Q samples
    accumulator #(
        .DATA_WIDTH(DATA_WIDTH)
    ) Q_acc (
        .clk(clk),
        .rst(rst),
        .en(done),
        .din(Q),
        .dout(total_Q)
    );

    // Signle port RAM for the I samples
    single_port_ram #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH)
    ) I_ram (
        .clk(clk),
        .we(we),
        .addr(addr),
        .din(I),
        .dout(stored_I)
    );

    // Signle port RAM for the Q samples
    single_port_ram #(
        .ADDR_WIDTH(ADDR_WIDTH),
        .DATA_WIDTH(DATA_WIDTH)
    ) Q_ram (
        .clk(clk),
        .we(we),
        .addr(addr),
        .din(Q),
        .dout(stored_Q)
    );

    // IQ Sample Counter
    iq_counter #(
        .WIDTH(ADDR_WIDTH)
    ) counter(
        .rst(rst),
        .clk(clk),
        .iq_count(addr)
    );

    assign I_dc = total_I / 2**ADDR_WIDTH;
    assign Q_dc = total_Q / 2**ADDR_WIDTH;

    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            we <= 1'b1;
            done <= 0;
        end
        else begin
            if (addr == 2**ADDR_WIDTH-1) begin
                we <= ~we;
                done <= ~done;
            end
        end
    end

endmodule