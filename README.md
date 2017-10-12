# sensors
Classes to help take measurements from sensors attached to the Raspberry Pi

The Raspberry Pi has no built-in means of reading PWM data.
Standard GPIO facilities can be used by repeatedly reading the input value
on a pin, and comparing the number of samples in a high vs a low reading.
The DHT11 and DHT22 sensors have a minimum high pulse width of 26 µs which
is just wide enough for this technique to work.
