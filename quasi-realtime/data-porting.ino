#include <ESP8266WiFi.h>

const char *ssid = "HOME-WIFI-SSID-CENSORED";
const char *password = "HOME-WIFI-PW-CENSORED";
const char *host = "CENSORED.000webhostapp.com";
bool autoReconnect = true;
bool autoConnect = true;
int ROOM = 1; // room number, old data reference
int X = 0;    // coordinates
int Y = 0;
int iteration = 1; // number of measurements made at that location (from 1-3)
int DUMMY = 1;

void setup()
{
    Serial.begin(115200);
    delay(1500); // ESP8266 waiting after boot up

    WiFi.mode(WIFI_STA);
    WiFi.setAutoReconnect(autoReconnect); // if WiFi client fails, reconnect
    WiFi.setAutoConnect(autoConnect);
}

void connect_WiFi()
{
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(100);
        // omitted serial printing, just in hopes that the connection works
    }
}

void loop()
{
    String ssid;
    int32_t rssi;
    uint8_t encryptionType;
    uint8_t *bssid;
    int32_t channel;
    bool hidden;
    int scanResult;
    String AProw;
    String rssistack;

    Serial.begin(115200);
    if (WiFi.status() != WL_CONNECTED){
        connect_WiFi();
    } if (WiFi.status() == WL_CONNECTED){
        Serial.println("Scanning networks.");
        iteration = 1;

        // removed all data collection code

        scanResult = WiFi.scanNetworks(/*async=*/false, /*hidden=*/true);
        // retrieve all available APs

        if (scanResult == 0){
            Serial.println("No networks found");
        }

        else if (scanResult > 0){
            rssistack = IpAddress2String(WiFi.localIP());
            rssistack += "%20";

            for (int i = 0; i < scanResult; i++){
                // Enter all data into the system, including rssi connections and timestamps
                WiFi.getNetworkInfo(i, ssid, encryptionType, rssi, bssid, channel, hidden);
                if (check2hex(bssid[0]) == "E4" && check2hex(bssid[1]) == "6F" && check2hex(bssid[2]) == "13" && check2hex(bssid[3]) == "45" && check2hex(bssid[4]) == "AB"){
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
                    // AProw += (encryptionType == ENC_TYPE_NONE) ? ' ' : '*';
                    // AProw += "|";
                    // AProw += hidden ? 'H' : 'V';
                    // AProw += "|";
                    // AProw += ssid.c_str();
                    // Serial.printf(PSTR("%02d: [CH %02d] [%02X:%02X:%02X:%02X:%02X:%02X] %ddBm %c %c %s\n"), i, channel, bssid[0], bssid[1], bssid[2], bssid[3], bssid[4], bssid[5], rssi, (encryptionType == ENC_TYPE_NONE) ? ' ' : '*', hidden ? 'H' : 'V', ssid.c_str());
                    rssistack += AProw;
                }
            }
            
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
        } else {
            Serial.printf("WiFi.scanNetworks failed");
        }

        // Sending data to server, with HTTP jargons
        Serial.println("Preparing for server.");
        WiFiClient clientGet;
        const int httpGetPort = 80;

        // prints all the data into serial
        serial.println(rssistack);
        
        delay(1000); // 5000:if the delay is too short, it will loop before printing APs
    }
}
}

String IpAddress2String(const IPAddress &ipAddress)
{
    return String("Time:") + String(millis() / 1000) + String("%20") + String(ipAddress[0]) + String(".") + String(ipAddress[1]) + String(".") + String(ipAddress[2]) + String(".") + String(ipAddress[3]);
}

String check2hex(int MAC)
{
    String newMAC;
    newMAC = String(MAC, HEX);
    if (MAC >= 15)
    {
        newMAC.toUpperCase();
    }
    else if (MAC >= 10 && MAC <= 15)
    {
        newMAC.toUpperCase();
        newMAC = "0" + newMAC;
    }
    else if (MAC < 10)
    {
        newMAC = "0" + newMAC;
    }
    return newMAC;
}

String check2digits(int integer)
{
    String twodigits;
    if (integer >= 0 && integer <= 9)
    {
        twodigits = "0";
        twodigits += String(integer, DEC);
    }
    else
    {
        twodigits = String(integer, DEC);
    }
    return twodigits;
}
