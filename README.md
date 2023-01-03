# code_injector
Inject HTML, CSS and JS while communication between client in server, MITM

Used with arp spoofer first become Man in the middle then use this to inject code.

Set iptables rule to this before using code_injector:
use set_rules.sh

Usage: code_injector.py [options]

Options:
  -h, --help            show this help message and exit
  -m MALACIOUSJS, --malacious-js=MALACIOUSJS
                        Enter Malacious javascript code (eg: -m
                        "<script>alert(1);</script>"

![Screenshot 2023-01-03 120824](https://user-images.githubusercontent.com/109381227/210311167-91b2692a-50c5-423d-96e9-59abd0220679.jpg)

Example:
python3 code_injector.py -m "<script>alert(1);</script>"

![Screenshot 2023-01-03 120938](https://user-images.githubusercontent.com/109381227/210311276-cb0d4d44-750a-4124-bb48-dc8361ea630c.jpg)

