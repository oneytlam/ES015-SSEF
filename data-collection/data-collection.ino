#include <ESP8266WiFi.h>

const char* ssid     = "HOME-WIFI-SSID-CENSORED";
const char* password = "HOME-WIFI-PW-CENSORED";
const char* host = "CENSORED.000webhostapp.com"; 
bool autoReconnect = true;
bool autoConnect = true;
int ROOM = 1; // room number, old data reference
int X = 0; // coordinates 
int Y = 0;
int iteration = 1;  // number of measurements made at that location (from 1-3)
int DUMMY=1;


void setup() {
  Serial.begin(115200);
  delay(1500); // ESP8266 waiting after boot up
  Serial.println();

  Serial.print("First boot to "); // first connection to home wifi for data uploading purposes
  Serial.println(ssid); // print the SSID of the network you're attached to
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(autoReconnect); // if WiFi client fails, reconnect
  WiFi.setAutoConnect(autoConnect);
}

void connect_WiFi(){
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("."); // attempt to connect to WiFi
    delay(100);
  }
  Serial.println("WiFi is connected.");  
}

void loop() {
  String ssid;
  int32_t rssi;
  uint8_t encryptionType;
  uint8_t* bssid;
  int32_t channel;
  bool hidden;
  int scanResult;
  String AProw;
  String rssistack;
  
  Serial.begin(115200);
  if (WiFi.status() != WL_CONNECTED) {
    connect_WiFi();
  }
  if (WiFi.status() == WL_CONNECTED) {
      Serial.println("Scanning networks.");
      iteration = 1;

      // the following is data collection for X and Y coordinates
      Serial.println("Please enter the X coordinate:"); 
      while (Serial.available() == 0) {}
      X = Serial.parseInt();
      Serial.println("X coordinate is: ");
      Serial.println(X);
      while (Serial.available() == 0) {}
      Y = Serial.parseInt();
      Serial.println("Please enter the Y coordinate:");
      while (Serial.available() == 0) {}
      Y = Serial.parseInt();
      Serial.println("Y coordinate is: ");
      Serial.println(Y);

      // Repeating process of network collection for 5 iterations
        Serial.println("iteration is: ");
        Serial.println(iteration);

        scanResult = WiFi.scanNetworks(/*async=*/false, /*hidden=*/true);
        // Retrieve all available APs

        if (scanResult == 0) {
          Serial.println("No networks found");
        } 
        else if (scanResult > 0) {
          Serial.printf("%d networks found.\n", scanResult);
          rssistack = IpAddress2String(WiFi.localIP());
          rssistack += "%20";
          
          for (int i = 0; i < scanResult; i++) {
            // Enter all data into the system, including rssi connections and timestamps
            WiFi.getNetworkInfo(i, ssid, encryptionType, rssi, bssid, channel, hidden);
            if (check2hex(bssid[0]) == "E4" && check2hex(bssid[1]) == "6F" && check2hex(bssid[2]) == "13" && check2hex(bssid[3]) == "45" && check2hex(bssid[4]) == "AB") {
              AProw = check2digits(i);
              AProw += "[";
              AProw += check2hex(bssid[0]);
              AProw += ":";
              AProw += check2hex(bssid[1]);
              AProw += ":";
              AProw += check2hex(bssid[2]);
              AProw += ":";
              AProw += check2hex(bssid[3]);
              AProw += ":";
              AProw += check2hex(bssid[4]);
              AProw += ":";
              AProw += check2hex(bssid[5]);
              AProw += "]";
              AProw += rssi;
              AProw += "d%20";   
              //AProw += (encryptionType == ENC_TYPE_NONE) ? ' ' : '*';
              //AProw += "|";
              //AProw += hidden ? 'H' : 'V';
              //AProw += "|";
              //AProw += ssid.c_str();
            //Serial.printf(PSTR("%02d: [CH %02d] [%02X:%02X:%02X:%02X:%02X:%02X] %ddBm %c %c %s\n"), i, channel, bssid[0], bssid[1], bssid[2], bssid[3], bssid[4], bssid[5], rssi, (encryptionType == ENC_TYPE_NONE) ? ' ' : '*', hidden ? 'H' : 'V', ssid.c_str());
              rssistack += AProw;
            }
          }
          while (Serial.available() == 0) {}
          DUMMY = Serial.parseInt();
          rssistack += "%20";
          rssistack += "Room";
          rssistack += ROOM;
          rssistack += "%20";
          rssistack += "(";
          rssistack += X;
          rssistack += ",";
          rssistack += Y;
          rssistack += ")";
          rssistack += "%20";
          rssistack += "Iteration";
          rssistack += iteration;
        }
        else {
          Serial.printf("WiFi.scanNetworks failed");
        }

        //Sending data to server, with HTTP jargons
        Serial.println("Preparing for server.");
        WiFiClient clientGet;
        const int httpGetPort = 80;

        // we modified the path during every experiment for different dat files
        String path = "/yiy5.php";
        String query = "?data=";
        String urlGet;
        urlGet += path + query + rssistack; //setup HTTP protocol: GET formatting "/server1.php?data="
        if (!clientGet.connect(host, httpGetPort)) {
          Serial.println("WiFiClient failed.");
        } 
        if (clientGet.connect(host, httpGetPort)) {
          clientGet.println("GET " + urlGet + " HTTP/1.1");
          clientGet.print("Host: ");
          clientGet.println(host);
          clientGet.println("Connection: close\r\n");

          //read back one line from server, usually it is the Server Response, i.e. "HTTP/1.1 200 OK"
          Serial.print("Server Response:");
          String line = clientGet.readStringUntil('\r');
          Serial.println(line);
          iteration++;
        }
        Serial.println("Closing host, reloop after 1s.");
        delay(1000); //5000:if the delay is too short, it will loop before printing APs
      }    
    }
    
  }

String IpAddress2String(const IPAddress& ipAddress)
{
    return String("Time:") + String(millis() / 1000) + String("%20") + String(ipAddress[0]) + String(".") + String(ipAddress[1]) + String(".") + String(ipAddress[2]) + String(".") + String(ipAddress[3]);
}

String check2hex(int MAC){
  String newMAC;
  newMAC = String(MAC,HEX);
  if (MAC >= 15) {
    newMAC.toUpperCase();
  }
  else if (MAC >= 10 && MAC <= 15){
    newMAC.toUpperCase();
    newMAC = "0"+newMAC;
  }
  else if (MAC<10){
    newMAC = "0"+newMAC;
  }
  return newMAC;  
}

String check2digits(int integer){
  String twodigits;
  if (integer >= 0 && integer <= 9) {
    twodigits = "0";
    twodigits += String(integer,DEC);
  }
  else {
    twodigits = String(integer,DEC);
  }
  return twodigits;
}
