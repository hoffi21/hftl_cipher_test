# hftl_cipher_test
### Finishing the class task for last semester - IT-Security

It's a simple python tool to see how long different TLS ciphers take to establish
a TCP connection. Furthermore it writes the results in an excel file (which the tool creates)
and creates a chart to compare several tested ciphers.

*it's hard-coded TLSv1.2*

To get a little bit of statistical reliability the tool establish 10 seperate TCP connections.
For writing in excel from python the xlsxwriter package is used.
