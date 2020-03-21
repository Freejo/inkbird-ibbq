# inkbird-ibbq
read inkbird ibbq ibt-2x thermometer values

This is entirely based on the awesome wotk done by https://github.com/pauledd/inkbird-ibbq

Please beare in mind that I am new to Python and new to Bluetooth readings.
If you can contribute improvements - Please do...

After going through several code examples of others and comparing battery level calculations,
For me a simple currentV / MaximumV * 100 just dis not seem accurate.

Battery level depends on temperature(same as your car battery behaves different in summer than in winter)
I am still not exactly sure how iBBQ calculates remaining battery percentage.
But according to the values read by Bluetooth snoop it (fr me) is quite close to what the readings say when opening my App.

All readings are inserted into a MySQL database on which i created a Grafana frontend to be able to get readings to my home(Raspberry PI 4) whenever 
I have to step out.

Againn great thanks to Paul who´s project helped me starting.

