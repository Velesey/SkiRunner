
int pin = A0;
int minSignal = 600;
bool stateUp = false;
bool lastState = false;
bool oneStep = false;
void setup() {
	pinMode(pin, INPUT);
	Serial.begin(9600);

}

void loop() {
	int signal = analogRead(pin);
	//Serial.println(signal);
	if (signal > minSignal){
		stateUp = true;
	}
	else{
		stateUp = false;
	}
	if (lastState != stateUp && lastState == false){
		//Serial.println(1);
		oneStep = not oneStep;
	}
	else {
		//Serial.println(0);

	}

	lastState = stateUp;
	Serial.println(oneStep);
}

