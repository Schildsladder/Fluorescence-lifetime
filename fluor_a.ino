uint16_t buf[3695];
void setup(){
  SerialUSB.begin(0);
  while(!SerialUSB);
  ADC->ADC_MR |= 0x80; // these lines set free running mode on adc 7 (pin A0)
  ADC->ADC_CR=2;
  ADC->ADC_CHER=0x80;
  attachInterrupt(19, state_change, RISING);
}

void loop(){
}

void state_change(){
  for(int i=0;i<3694;i++){
    while((ADC->ADC_ISR & 0x80)==0); 
    buf[i]=ADC->ADC_CDR[7];
  }
  buf[3694] = 12500;
  SerialUSB.write((uint8_t *)buf,7390);
//  delay(1);
}
