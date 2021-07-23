from optparse import OptionParser


class MyOptionParser(OptionParser):
    def format_epilog(self, formatter):
        return self.epilog

parser = MyOptionParser(description="xxxxxx",
                        epilog='''
Examples:
  xxxx:
  python xxx.zip -a 'xxx' -i 'xxx'
''')
parser.add_option("-a", dest="item1",
                  help="xxxxxxxxx")
parser.add_option("-i", dest="item2",  default="xxx",
                  help="[integration] IP address or host name of agent")
parser.add_option("-n", dest="xxx", type="int", default=4,
                  help="xxx [default: 4]")
parser.add_option("-R", "--xxxxx", dest="xxxxx", action="store_true", default=False,
                  help="xxxxxxx")

(options, args) = parser.parse_args()
