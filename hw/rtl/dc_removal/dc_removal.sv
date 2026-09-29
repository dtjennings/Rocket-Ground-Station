////////////////////////////////////////////////////////////
// This is the top level rtl for the DC Offset Removal IP
////////////////////////////////////////////////////////////

module dc_removal #(
    parameter WIDTH = 10
)(

);

    logic [WIDTH:0]addr;

    iq_counter #(
        .WIDTH(WIDTH)
    ) inst(
        .en(),
        .rst(),
        .clk(),
        .iq_count()
    );

endmodule