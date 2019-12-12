//uint16_t buf[4][256];
uint16_t buf[7389];
int scale=50;
int scale1=3700;
int scale2=3700;
String inString = "";

void setup() {

  pinMode(33, OUTPUT);
  pinMode(34, OUTPUT);
  pinMode(35, OUTPUT); 

  REG_PIOC_OWER = 0x0000000e; //  pin 35, pin 34, pin 33
  REG_PIOC_OWDR = 0xfffffff1;
}

void loop() {
//pin 35, pin 34, pin 33
  for(int j=0;j<9;j++){
    REG_PIOC_ODSR = 0x00000006; //0110
    REG_PIOC_ODSR = 0x00000006;
    delayMicroseconds(300);
    REG_PIOC_ODSR = 0x00000004; //0100
    REG_PIOC_ODSR = 0x00000004;
    delayMicroseconds(500);
  }
  delayMicroseconds(9000);
//  for(int i=0;i<80;i++){
//      REG_PIOC_ODSR = 0x00000004; //0100
//      REG_PIOC_ODSR = 0x00000004;
//    }
}
