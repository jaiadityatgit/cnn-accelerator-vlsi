module conv3x3(
    input clk,
    input reset,

    input [7:0] p1, input [7:0] p2, input [7:0] p3,
    input [7:0] p4, input [7:0] p5, input [7:0] p6,
    input [7:0] p7, input [7:0] p8, input [7:0] p9,

    input [7:0] k1, input [7:0] k2, input [7:0] k3,
    input [7:0] k4, input [7:0] k5, input [7:0] k6,
    input [7:0] k7, input [7:0] k8, input [7:0] k9,

    output reg [31:0] result
);

wire [15:0] m1 = p1 * k1;
wire [15:0] m2 = p2 * k2;
wire [15:0] m3 = p3 * k3;
wire [15:0] m4 = p4 * k4;
wire [15:0] m5 = p5 * k5;
wire [15:0] m6 = p6 * k6;
wire [15:0] m7 = p7 * k7;
wire [15:0] m8 = p8 * k8;
wire [15:0] m9 = p9 * k9;

wire [31:0] sum = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8 + m9;

always @(posedge clk or posedge reset) begin
    if (reset)
        result <= 0;
    else
        result <= sum;
end

endmodule