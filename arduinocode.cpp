#include <FastLED.h>

#define LED_PIN 6       // Pin connected to the LED strip
#define NUM_LEDS 30     // Number of LEDs in the strip

CRGB leds[NUM_LEDS];    // Array to store LED colors

void setup() {
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);  // Initialize the LED strip
  FastLED.setBrightness(100);    // Set the LED brightness (0-255)
  Serial.begin(9600);            // Initialize serial communication at 9600 bps
}

void loop() {
  if (Serial.available() > 0) {   // Check if there is incoming serial data
    char incomingByte = Serial.read();  // Read the incoming byte

    if (incomingByte == '1') {
      // Turn on the LED strip with a specific color
      fill_solid(leds, NUM_LEDS, CRGB::Red);
      FastLED.show();
    } else if (incomingByte == '0') {
      // Turn off the LED strip
      fill_solid(leds, NUM_LEDS, CRGB::Green);
      FastLED.show();
    }
  }
}

