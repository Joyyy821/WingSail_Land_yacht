#include <Servo.h>

// Slave:
// Receive command from master and send corresponding command to servo 1/2.
// Command:
// S/R + A/D + degree: sail/front wheel turns left/right for a given degree.
// Q/W + A/D + degree: sail/front wheel turns TO the position of left/right angle with the given degree.
// Z/X: sail/front wheel turns back to the course direction.

Servo sail_ser;
Servo rud_ser;
int sail_pos = 95;     // 0 - 180
int rud_pos = 135;      // 100 - 165


void setup() {
  // put your setup code here, to run once:
  sail_ser.attach(9);//the servo control used PWM
  rud_ser.attach(10);//the servo control used PWM2
  Serial.begin(9600);
  delay(500);
  while (Serial.read() >= 0) {} //清除可能存在的缓存
  sail_ser.write(sail_pos);
//  delay(150);
//  sail_ser.write(-sail_pos);
  rud_ser.write(rud_pos);
  Serial.println("Set up for Slave is finished.");
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available()){
    int inChar = Serial.read();
    int delta_pos;
    delta_pos = decide_angle();
    if ((char)inChar == 'Z') {
      sail_pos = 95;
      sail_ser.write(sail_pos);
      Serial.println("Z");
    }
    if ((char) inChar == 'X') {
      rud_pos = 135;
      rud_ser.write(rud_pos);
      Serial.println("X");
    }
    if ((char)inChar == 'S') {
      sail_pos += delta_pos;
      if (sail_pos > 180) {
        sail_pos = 180;
      } else if (sail_pos < 0) {
        sail_pos = 0;
      }
      sail_ser.write(sail_pos);
      Serial.print("Sail servo turns ");
      Serial.println(delta_pos);
      Serial.println(delta_pos);
      Serial.print("Current sail servo pos: ");
      Serial.println(sail_pos);
    } else if ((char)inChar == 'R') {
      rud_pos += delta_pos;
//      if (rud_pos > 165) {
//        rud_pos = 165;
//      } else if (rud_pos < 100) {
//        rud_pos = 100;
//      }
      rud_ser.write(rud_pos);
      Serial.print("Rudder servo turns ");
      Serial.println(delta_pos);
      Serial.println(delta_pos);
      Serial.print("Current rudder servo pos: ");
      Serial.println(rud_pos);
//      delay(150);
//      rud_ser.write(-rud_pos);
    } 
    if ((char)inChar == 'Q') {
      sail_pos = 95 + delta_pos;
      sail_ser.write(sail_pos);
      Serial.print("Sail servo position: ");
      Serial.println(sail_pos);
    } else if ((char)inChar == 'W') {
      rud_pos = 135 + delta_pos;
      rud_ser.write(rud_pos);
      Serial.print("Rudder servo position: ");
      Serial.println(rud_pos);
    }
//    Serial.println();
//    else {
//      Serial.println("Invalid servo.");
//    }
  }

  delay(500);
}

// TODO: 不确定向左向右的正负号
int decide_angle() {
  int cmd;
  if (Serial.available()){
    cmd = Serial.read();
    if (cmd == 'D') {
      return -read_abs_angle();
    } else if (cmd == 'A') {
      return read_abs_angle();
    } 
//    else {
//      Serial.println("Invalid command.");
//    }
  }
  
}

// TODO: 没有处理异常的角度输入 & 角度输入必须为正
int read_abs_angle() {
  int current_char;
  String inString = "";
  while (true) {
    if (Serial.available()){
      current_char = Serial.read();
      // 注意：因为我们必须把指令读入之后在判断是否为数字，所以这个函数会消耗指令之后的一个字符才能break（建议每次传输指令时在角度后加一个空格啥的）
      if (isDigit(current_char)) {
        inString += (char)current_char;
      } else {
        break;
      }
    } else {
      break;
    }
  } 
  return inString.toInt();
}
