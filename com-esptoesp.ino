
#include <esp_now.h>
#include <WiFi.h>
#define solenoide 5
#define solenoide2 4
// Structure example to receive data
// Must match the sender structure
typedef struct struct_message {
    char a[32];
    int b;
    float c;
    bool d;
} struct_message;
// Create a struct_message called myData
struct_message myData;
// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&myData, incomingData, sizeof(myData));
 
  if(myData.b == 1){
    Serial.println("UM");
    digitalWrite(solenoide, LOW);
    digitalWrite(solenoide2, HIGH);
  }
    else if(myData.b == 2){
    Serial.println("DOIS");
    digitalWrite(solenoide, HIGH);
    digitalWrite(solenoide2, LOW);
  }
  else if(myData.b == 0){
    digitalWrite(solenoide, LOW);
    Serial.println("TRES");
    digitalWrite(solenoide2, LOW);
  }
}
void setup() {
  // Initialize Serial Monitor
  pinMode(solenoide, OUTPUT);
   pinMode(solenoide2, OUTPUT);
  Serial.begin(115200);
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  // Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}
 
void loop() {
}