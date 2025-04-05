This bash script generates a keyprint of a particular certificate in Linux, as used in the KEYP extension.

The script uses OpenSSL, filters all the verbosity OpenSSL adds and then uses Python to encode it into Base32.

The script first calls OpenSSL to get the fingerprint then remove the verbosity and the colons convert with Python and remove any padding.

How to use:
./keyp_keyprint_generation.sh file

Where 'file' is the name and path of the certificate file.

Example:
./keyp_keyprint_generation.sh /etc/adchpp/certs/cacert.pem