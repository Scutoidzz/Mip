import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse_html.parse import parser
from grab.pull import pull_raw

# First try with the string and then 
test_html = "<html><body><h1>Hello World</h1><p>This is a test</p></body></html>"
print(parser(test_html))

os.system('clear' if os.name == 'posix' else 'cls')
print(parser(pull_raw("http://echo.free.beeceptor.com/")[0].decode('utf-8')))

os.system('clear' if os.name == 'posix' else 'cls')
if parser(pull_raw("http://echo.free.beeceptor.com/")[0].decode('utf-8'))[0][0] == 'text':
    print("Tests successful :)")
else:
    print("Tests failed :(")