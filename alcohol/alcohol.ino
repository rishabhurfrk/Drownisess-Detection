#define alcohol A0
int relay=4;

int in1=6;
int in2=7;
int in3=8;
int in4=9;

int red=10;
int yellow=11;
int green=12;

int x;
int sensor_value;

void movement(){
   digitalWrite(in1,HIGH);
   digitalWrite(in2,LOW);
   digitalWrite(in3,LOW);
   digitalWrite(in4,HIGH);
} 

void pause(){
   digitalWrite(in1,LOW);
   digitalWrite(in2,LOW);   
   digitalWrite(in3,LOW);
   digitalWrite(in4,LOW); 
}  

void function(bool red1, bool yellow1, bool green1, bool relay1){
  digitalWrite(red,red1);
  digitalWrite(yellow,yellow1);
  digitalWrite(green,green1);
  digitalWrite(relay,relay1);
}  

void setup() {
  Serial.begin(9600);

  // led
  pinMode(red,OUTPUT);
  pinMode(yellow,OUTPUT);
  pinMode(green,OUTPUT);

  // alcohol
  pinMode(alcohol,INPUT);

  // motor
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);

  // relay
  pinMode(relay,OUTPUT);
  digitalWrite(relay,HIGH);

  Serial.setTimeout(1);

}

void loop() {

//    while(!Serial.available());
     
    x = Serial.readString().toInt();
  
    sensor_value=analogRead(alcohol);
    float voltage=sensor_value*(5.0/1023.0);
    float alcoholConcentration = (voltage - 0.1) / 0.8 * 100;

//    Serial.println(sensor_value);
    Serial.println(alcoholConcentration);
    delay(1000);
    if(alcoholConcentration > 50){
      //Serial.println(alcoholConcentration);
      function(1,0,0,0);
      pause();
    }
    else if(alcoholConcentration < 50){
      function(0,0,0,0);
      pause();
    }
    
    else{
      if(x==2){
        function(0,1,0,0);
        pause();
      }
      else if(x==3){
        function(0,1,0,0);
        pause(); 
      }
      else if(x==4){
//      Serial.println(0);
        function(0,0,1,1);
        movement();
      }  
   
    }
    
}
