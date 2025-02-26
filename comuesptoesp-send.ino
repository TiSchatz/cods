#include <esp_now.h>
#include <WiFi.h>
#define solenoide 4
#define solenoide2 5
// REPLACE WITH YOUR RECEIVER MAC Address
uint8_t broadcastAddress[] = {0x10, 0x06, 0x1C, 0x85, 0x7D, 0xFC};// ENDEREÇO DO ESCRAVO
String entrada = " ";
// Structure example to send data
// Must match the receiver structure
typedef struct struct_message {
  char a[32];
  int b;
  float c;
  bool d;
} struct_message;

// Create a struct_message called myData
struct_message myData;

esp_now_peer_info_t peerInfo;

// callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  //Serial.print("\r\nLast Packet Send Status:\t");
 // Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  // Init Serial Monitor
  Serial.begin(115200);
   pinMode(solenoide,  INPUT_PULLDOWN);
   pinMode(solenoide2,  INPUT_PULLDOWN);


  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Once ESPNow is successfully Init, we will register for Send CB to
  // get the status of Trasnmitted packet
  esp_now_register_send_cb(OnDataSent);
  
  // Register peer
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Add peer        
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }
}
 
void loop() {
  // Set values to send
 // strcpy(myData.a, "THIS IS A CHAR");
 // myData.b = 1;
  //myData.c = 1.2;
  //myData.d = false;
  /*
  if (Serial.available()) {  // Verifica se há dados no Serial
    String entrada = Serial.readStringUntil('\n'); // Lê até a quebra de linha
    entrada.trim(); // Remove espaços extras

    Serial.print("Você digitou: ");
    Serial.println(entrada);
  */
  int pinState = digitalRead(4);
  int pinState2 = digitalRead(5);
  
    if (pinState == HIGH) { // Verifica se é "OK"
      strcpy(myData.a, "right");
      Serial.println("right");
      myData.b = 1;
    } else  if(pinState2 == HIGH) {
      strcpy(myData.a, "WRONG");
      Serial.println("WRONG");
      myData.b = 2;
    }else if (pinState == LOW && pinState2 == LOW){
      myData.b = 0;
      Serial.println("DEsligados");
    }

  
  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
   
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }
  
  
}