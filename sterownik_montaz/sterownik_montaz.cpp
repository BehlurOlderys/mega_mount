#include <Arduino.h>

const int NUMBER_OF_TEETH = 130;  // for EQ 3-2
const long int SIDEREAL_DAY_SECONDS = 86164;
const long int NUMBER_OF_ENCODER_STEPS = 1600; // 4*400 in

// 86164 seconds = 1600 * 130 steps = 208000 steps
//

const int TOTAL_STEPS_BY_1000 = ( NUMBER_OF_TEETH * NUMBER_OF_ENCODER_STEPS ) / 1000;
const long int STEP_INTERVAL_MICROS = (long int)( SIDEREAL_DAY_SECONDS * 1000 ) / (long int)(TOTAL_STEPS_BY_1000); // 414250;

unsigned long last_time_us = 0;
unsigned long current_time_us = 0;
long int cummulative_delta_us = 0;

const int PIN_RA_PLUS = 6;
const int PIN_RA_MINUS = 5;
const int PIN_DEC_PLUS = 4;
const int PIN_DEC_MINUS = 3;

const int COMMAND_MAX_LENGTH = 20;
const int COMMAND_NAME_LENGTH = 10;
char command_string[COMMAND_MAX_LENGTH];
char command_name[COMMAND_NAME_LENGTH];
char command_trash[COMMAND_MAX_LENGTH];

void reset_pins(){
  digitalWrite(PIN_RA_PLUS, 0);
  digitalWrite(PIN_RA_MINUS, 0);
  digitalWrite(PIN_DEC_PLUS, 0);
  digitalWrite(PIN_DEC_MINUS, 0);
}


const int BAD = 0;
int table_of_states[4][4] = {
  {  0,   1,  -1, BAD},
  { -1,   0, BAD,   1},
  {  1, BAD,   0,  -1},
  {BAD,  -1,   1,   0}
};
int current_angle = 0;
int previous_index = 0;
long int perfect_angle = 0;

void setup() {
  // put your setup code here, to run once:

  pinMode(PIN_RA_PLUS, OUTPUT);
  pinMode(PIN_RA_MINUS, OUTPUT);
  pinMode(PIN_DEC_PLUS, OUTPUT);
  pinMode(PIN_DEC_MINUS, OUTPUT);

  reset_pins();

  Serial.begin(115200);

  pinMode(A1, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);

  current_angle = 0;
  current_time_us = micros();
  last_time_us = current_time_us;
  cummulative_delta_us = 0;
  perfect_angle = 0;
}

void action(int pin_to_set, int time_to_move){
//  Serial.print("setting pin no: ");
//  Serial.print(pin_to_set);
//  Serial.print(" by amount: ");
//  Serial.println(time_to_move);

  digitalWrite(pin_to_set, 1);
  delay(time_to_move);
  reset_pins();

}

unsigned int lastA = 2;
unsigned int lastB = 2;

// A  B    A' B'   index index' increment
// 0  0    0  0    0     0      0
// 0  0    0  1    0     1      1
// 0  0    1  0    0     2     -1
// 0  0    1  1    0     3      X

// 0  1    0  0    1     0     -1
// 0  1    0  1    1     1      0
// 0  1    1  0    1     2      X
// 0  1    1  1    1     3      1

// 1  0    0  0    2     0      1
// 1  0    0  1    2     1      X
// 1  0    1  0    2     2      0
// 1  0    1  1    2     3     -1

// 1  1    0  0    3     0      X
// 1  1    0  1    3     1     -1
// 1  1    1  0    3     2      1
// 1  1    1  1    3     3      0

// 0->[0, 1, -1, 0]
// 1->[-1, 0, 0, 1]
// 2->[1, 0, 0, -1]
// 3->[0, -1, 1, 0]

void print_state(long int error_angle){
  Serial.print(current_time_us);
  Serial.print(" ");
  Serial.print(current_angle);
  Serial.print(" ");
  Serial.print(error_angle);
  Serial.print(" ");
  Serial.println(cummulative_delta_us);
}

void command_control(const long int error_angle){
  if (error_angle < -1){
    reset_pins();
    digitalWrite(PIN_RA_PLUS, HIGH);
  }
  else if (error_angle > 1){
    reset_pins();
    digitalWrite(PIN_RA_MINUS, HIGH);
  }
  else if (error_angle == 0){
    reset_pins();
  }
}

void autonomous_control(){
   unsigned int channelA = analogRead (A1) > 512;
   unsigned int channelB = analogRead (A2) > 512;

   const byte current_index = 2*channelA + channelB;
   const int angle_progress = table_of_states[previous_index][current_index];
   current_angle += angle_progress;


   if (current_index != previous_index){
     current_time_us = micros();
     const long int delta_us = current_time_us - last_time_us;
     const long int new_cummulative = (cummulative_delta_us + delta_us);
     perfect_angle += new_cummulative / STEP_INTERVAL_MICROS;
     cummulative_delta_us = new_cummulative % STEP_INTERVAL_MICROS;
     const long int error_angle = perfect_angle - current_angle;
     print_state(error_angle);
     command_control(error_angle);
   }
//    command_control(error_angle);
   print_counter++;
   if (print_counter > 100){
     print_counter = 0;
//      print_state(error_angle);
//      command_control(error_angle);
   }


   previous_index = current_index;
   last_time_us = current_time_us;
}

void manual_control_via_serial(){
   memset(command_string, 0, COMMAND_MAX_LENGTH);
   memset(command_name, 0, COMMAND_NAME_LENGTH);
   int command_argument = 0;
   int pin_to_move = -1;

   Serial.readBytesUntil('\n', command_string, COMMAND_MAX_LENGTH);
   sscanf(command_string, "%s %d", command_name, &command_argument);
   if (0 == strcmp(command_name, "DEC_PLUS")){
     pin_to_move = PIN_DEC_PLUS;
   }else if (0 == strcmp(command_name, "DEC_MINUS")){
     pin_to_move = PIN_DEC_MINUS;
   }else if (0 == strcmp(command_name, "RA_PLUS")){
     pin_to_move = PIN_RA_PLUS;
   }else if (0 == strcmp(command_name, "RA_MINUS")){
     pin_to_move = PIN_RA_MINUS;
   }else{
     Serial.print("UNKNOWN COMMAND: ");
     Serial.print(command_string);
     Serial.println("!");
   }
   if (pin_to_move > 0){
     action(pin_to_move, command_argument);
   }
}

long int print_counter = 0;
void loop() {
  if (not Serial.available())
  {
     autonomous_control();
  }
  else
  {
     manual_control_via_serial();
  }
}
