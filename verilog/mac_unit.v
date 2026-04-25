module mac_unit(
    input clk,
    input [7:0] a,
    input [7:0] b,
    input reset,
    output reg [15:0] result
);

always @(posedge clk or posedge reset) begin
    if (reset)
        result <= 0;
    else
        result <= result + (a * b);
end

endmodule