#include <iostream>
#include <string>

using namespace std;

string  current_sensor (uint16_t read_digital_current)
 {

	 float sensitivity = 0.1; // 0.1 for 20A Model
	 float output_voltage = (float) read_digital_current * 3.3 * 2*1.035 / 4095;
	     // If output_voltage is not 2.5Volt, multiply by a factor.In my case it is 1.035
	     // This is due to tolerance in voltage divider resister & ADC accuracy
	 float current =(output_voltage - 2.5)/sensitivity;
	
	 string current_to_send = to_string (current);


     return current_to_send;
  }
 
int main()
{
    
   float sensor= -1.325;
    string s = to_string (sensor);
    cout << s << endl;
 
    return 0;
}