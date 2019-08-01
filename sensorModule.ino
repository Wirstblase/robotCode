#include <dht.h>
#define DHT11PIN 4
dht DHT;
int valoare;
int senzor_fum=A0;
int senzor_gaz=A1;
int sensorthres_fum=300;
int sensorthres_gaz=240;
int buzzer=6;
int vib_pin=7;
int v;
int inputPin = 2;               
int pirState = LOW;
int k=0;             
void buzz(){
 
  tone(buzzer, 5000); 
  delay(1000);        
  noTone(buzzer);    
  delay(1000);       
  
}


void setup() {
  
  Serial.begin(9600);
  delay(5000);
  Serial.println("BOII");
  pinMode(senzor_fum,INPUT);
  pinMode(senzor_gaz,INPUT);
  pinMode(inputPin, INPUT);
  pinMode(vib_pin,INPUT);
  // put your setup code here, to run once:

  Serial.println("PROGRAM STARTED");

}

void loop() {
      k++;
  //umiditate&temperatura
  int chk = DHT.read11(DHT11PIN);

  Serial.print("Umiditate (%): ");
  Serial.println((float)DHT.humidity, 2);

  Serial.print("Temperatura(C): ");
  Serial.println((float)DHT.temperature, 2);

  int senzor = 0;
    
  delay(2000);
  //gaz
  senzor = analogRead(senzor_gaz);
  Serial.print("gaz:");
  Serial.println(senzor);
  if (senzor > sensorthres_gaz && k>5)
  {
      Serial.println("gaz");
       buzz();
       delay(1000);  
  }
  else
    {
   noTone(buzzer);
      Serial.println("nogaz");
     
    }
    //fum
   senzor = analogRead(senzor_fum);
  Serial.print("valfum:");
  Serial.println(senzor);
 
  if (senzor > sensorthres_fum && k>5)
  {
      Serial.println("fum");
       buzz();
       delay(1000);  
  }
  else
   {
   noTone(buzzer);
      Serial.println("nofum");
     
    }
    //vibratie
  int v;
    v=digitalRead(vib_pin);
    Serial.print("valvibratie:");
    Serial.println(v);
  if(v==1)
  {
   delay(4000);  
     Serial.println("vibratie"); 
  buzz();       
  delay(4000);  
  }
  else
  {
   noTone(buzzer);
      Serial.println("novibratie");
     
  }
    delay(4000);
  //miscare
  valoare = digitalRead(inputPin);  
  if (valoare == HIGH)
      Serial.println("miscare");
      else
      Serial.println("nomiscare");      
  }
