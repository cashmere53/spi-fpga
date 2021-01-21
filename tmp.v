

module test #
(
  parameter INTERVAL = 125.0
)
(

);

  reg SCLK;
  reg RST;
  reg CS;
  reg [8-1:0] INPUT;
  wire [8-1:0] OUTPUT;

  spi-receiver
  #(
    .INTERVAL(INTERVAL)
  )
  uut
  (
    .SCLK(SCLK),
    .RST(RST),
    .CS(CS),
    .INPUT(INPUT),
    .OUTPUT(OUTPUT)
  );


  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut, SCLK, RST, CS, INPUT, OUTPUT);
  end


  initial begin
    SCLK = 0;
    forever begin
      #5 SCLK = !SCLK;
    end
  end


  initial begin
    RST = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #1000;
    $finish;
  end


endmodule



module spi-receiver #
(
  parameter INTERVAL = 125.0
)
(
  input SCLK,
  input RST,
  input CS,
  input [8-1:0] INPUT,
  output reg [8-1:0] OUTPUT
);

  reg [32-1:0] count;
  reg COMM_CLK;

  always @(posedge SCLK) begin
    if(RST) begin
      count <= 0;
      COMM_CLK <= 0;
    end else begin
      $display("count:%d");
      count
      if(count < INTERVAL - 1) begin
        count <= count + 1;
      end 
      if(count == INTERVAL - 1) begin
        count <= 0;
      end 
      if(count == INTERVAL - 1) begin
        COMM_CLK <= ~COMM_CLK;
      end 
    end
  end


endmodule

