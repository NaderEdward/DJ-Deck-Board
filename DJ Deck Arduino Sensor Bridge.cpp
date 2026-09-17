const int TRIG_1 = 2;
const int ECHO_1 = 3;
const int TRIG_2 = 4;
const int ECHO_2 = 5;
const int TOUCH_PIN = 11;

long getDistanceCM(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH, 25000); 
  if (duration == 0) return -1;
  return duration * 0.0343 / 2;
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_1, OUTPUT);
  pinMode(ECHO_1, INPUT);
  pinMode(TRIG_2, OUTPUT);
  pinMode(ECHO_2, INPUT);
  pinMode(TOUCH_PIN, INPUT);
}

void loop() {
  long dist1 = getDistanceCM(TRIG_1, ECHO_1);
  long dist2 = getDistanceCM(TRIG_2, ECHO_2);
  int touchState = digitalRead(TOUCH_PIN);

  // Stream raw ID-tagged data
  if (dist1 > 0) { Serial.print("US1="); Serial.println(dist1); }
  if (dist2 > 0) { Serial.print("US2="); Serial.println(dist2); }
  Serial.print("TOUCH="); Serial.println(touchState);

  delay(30); // ~33Hz polling rate
}