// Master:
// Receive command from computer and send the command to slave, or the reverse link.
// 相当于上位机的蓝牙收发器，loop中无需进行任何操作。

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500);
  while (Serial.read() >= 0) {} //清除可能存在的缓存
  Serial.println("Set up for Master is finished.");
}

void loop() {
  // Empty loop test.
  delay(500);
}
