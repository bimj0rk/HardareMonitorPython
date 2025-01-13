#include <Adafruit_GFX.h>    
#include <MCUFRIEND_kbv.h>   
#include "pics.h"

MCUFRIEND_kbv tft;

int xNamePos = 66;
int yNamePos[2] = {18 , 44};
int txtSize = 6;
int componentNameTxtSize = 2;
int componentSelector;
String *inData;
int idText;
String allData[3][4] = {
  {"    Intel     ", "   i5-9600k   ", "    nVidia    ", "   GTX 1060   "}, 
  {"   ", "   ", "   ", "   "},
  {"   ", "   ", "   ", "   "}
};
static const uint8_t *main_img[] = {cpu_img, gpu_img, mobo_img, case_img};
static const uint8_t *sensors_img[2][3] = {
  {temp_img, usage_img, ram_img},
  {temp_img, usage_img, fps_img}
};
static const uint8_t *symbols_img[2][3] = {
  {tempSymbol_img, usageSymbol_img, usageSymbol_img},
  {tempSymbol_img, usageSymbol_img, fpsSymbol_img}
};
boolean printName = false;

void setup() {
  Serial.begin(115200);
  uint16_t ID = tft.readID();
  if (ID == 0xD3) ID = 0x9481;
  tft.begin(ID);
  tft.setRotation(1);
  tft.fillScreen(TFT_BLACK);
  for (int i = 0; i < 2; i++) {
    int x = 240 * i;
    tft.drawRect(x + 1, 1, 63, 63, TFT_BLUE);
    tft.drawRect(x, 0, 63, 63, TFT_DARKGREY);
    tft.fillRect(x + 60, 5, 20, 25, TFT_BLACK);

    tft.drawRect(x + 1, 1, 239, 255, TFT_BLUE);
    tft.drawRect(x, 0, 239, 255, TFT_DARKGREY);

    tft.drawRect(x + 1, 257, 239, 63, TFT_BLUE);
    tft.drawRect(x, 256, 239, 63, TFT_DARKGREY);
    tft. drawLine(x + 18, 65, x + 18, 225, TFT_BLUE); 
    tft. drawLine(x + 17, 64, x + 17, 224, TFT_DARKGREY);
    for (int r = 1; r < 4; r++) {
      int y = 64 * r;
  
      tft.drawLine(x + 84 + 1, y + 1, x + 237 + 1, y + 1, TFT_BLUE);
      tft.drawLine(x + 84, y, x + 237, y, TFT_DARKGREY);

      tft.drawLine(x + 18, y + 32 + 1, x + 36, y + 32 + 1, TFT_BLUE);
      tft.drawLine(x + 17, y + 32, x + 35, y + 32, TFT_DARKGREY);

      tft.drawRect(x + 36, y + 8, 48, 48, TFT_DARKGREY);
      tft.drawRect(x + 35, y + 7, 48, 48, TFT_BLUE);
    }
  }

  for (int i = 0; i < 2; i++) {
    int x = 240 * i;

    tft.drawBitmap(x + 1, 1, main_img[i], 64, 64, TFT_DARKGREY);
    tft.drawBitmap(x, 0, main_img[i], 64, 64, TFT_BLUE);

    tft.drawBitmap(x + 1, 257, main_img[i + 2], 64, 64, TFT_DARKGREY);
    tft.drawBitmap(x, 256, main_img[i + 2], 64, 64, TFT_BLUE);

    tft.drawBitmap(x + 193, 265, symbols_img[0][0], 48, 48, TFT_WHITE);
    tft.drawBitmap(x + 192, 264, symbols_img[0][0], 48, 48, TFT_BLUE);
    for (int ii = 1; ii < 4; ii++) {
      int y = 64 * ii;

      tft.drawBitmap(x + 36, y + 9, sensors_img[i][ii - 1], 48, 48, TFT_DARKGREY);
      tft.drawBitmap(x + 35, y + 8, sensors_img[i][ii - 1], 48, 48, TFT_BLUE);

      tft.drawBitmap(x + 193, y + 9, symbols_img[i][ii - 1], 48, 48, TFT_WHITE);
      tft.drawBitmap(x + 192, y + 8, symbols_img[i][ii - 1], 48, 48, TFT_BLUE);
    }
  }

  printName = true;
  printData();
}

void loop(){
  printName = true;
  while(Serial.available() > 0){
    String recieved = Serial.readStringUntil(';');
    if (recieved.indexOf(':') != -1 ){
      int lastIndex = recieved.indexOf(':');
      int nextIndex;
      componentSelector = recieved[lastIndex - 1] - '0';
      switch (componentSelector) {
        case 0:
          printName = true;
        case 1:
        case 2:
          for (int i = 0; i < 4; i ++) {
            nextIndex = recieved.indexOf(',', lastIndex + 1);
            allData[componentSelector][i] = recieved.substring(lastIndex + 1, nextIndex);
            lastIndex = nextIndex;
          }
          break;
        case 3:
          printData();
          break;
      }
    }
  }
}

void printData(){
  if(printName == true){
    tft.setTextSize(componentNameTxtSize);
    tft.setTextColor(TFT_BLUE, TFT_BLACK);
    for(int i = 0; i < 4; i++){
      int x = 241 * (i / 2);
      tft.setCursor(xNamePos + x, yNamePos[i % 2]);
      tft.print(allData[0][i]);
    }
    printName = false;
  }

  tft.setTextSize(txtSize);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  for(int i = 0; i < 2; i++){
    int x = 90 + (241 * i);
    for(int ii = 1; ii < 5; ii++){
      int y = 10 + (64 * ii);
      tft.setCursor(x, y);
      tft.print(allData[i + 1][ii - 1]);
    }
  }
}
